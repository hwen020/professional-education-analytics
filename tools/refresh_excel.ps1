param([string]$Workbook = (Join-Path $PSScriptRoot '../deliverables/analysis-workbook.xlsx'))

$ErrorActionPreference = 'Stop'
$path = (Resolve-Path -LiteralPath $Workbook).Path
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false
$book = $null

function Assert-Near($actual, $expected, $label) {
    if ($null -eq $actual -or [Math]::Abs([double]$actual - [double]$expected) -gt 0.000001) {
        throw "$label failed. Expected $expected, got $actual"
    }
}

try {
    $book = $excel.Workbooks.Open($path, 0, $false)
    if ($book.ReadOnly) { throw 'Workbook is open read-only.' }
    $book.ForceFullCalculation = $true
    $explorer = $book.Worksheets.Item('Public FTES Explorer')
    $data = Import-Csv (Join-Path (Split-Path $path) 'public-cdcp-ftes.csv')
    $state = $data | Where-Object { $_.district -eq 'California statewide' -and $_.fiscal_year -eq '2024-25' }
    $district = $data | Where-Object { $_.district -eq 'Allan Hancock' -and $_.fiscal_year -eq '2024-25' }
    $pivotSheet = $null
    foreach ($sheet in $book.Worksheets) {
        if ($sheet.Name -eq 'Public FTES Pivot') { $pivotSheet = $sheet; break }
    }
    if ($null -eq $pivotSheet) {
        $pivotSheet = $book.Worksheets.Add()
        $pivotSheet.Name = 'Public FTES Pivot'
        $pivotSheet.Range('A1').Value2 = 'Public observations - CDCP FTES by area and fiscal year'
        $pivotSheet.Range('A2').Value2 = 'Statewide and district figures overlap. Totals across areas or years are disabled.'
        $cache = $book.PivotCaches().Create(1, 'PublicFTES')
        $pivot = $cache.CreatePivotTable($pivotSheet.Range('A5'), 'PublicFTESPivot')
        $pivot.PivotFields('district').Orientation = 1
        $pivot.PivotFields('fiscal_year').Orientation = 2
        $pivot.RowGrand = $false
        $pivot.ColumnGrand = $false
        $value = $pivot.AddDataField($pivot.PivotFields('ftes'), 'Published FTES', -4157)
        $value.NumberFormat = '#,##0.00'
    } else {
        $pivot = $pivotSheet.PivotTables('PublicFTESPivot')
    }
    $pivot.PivotCache().Refresh()
    if (-not $pivot.RefreshTable()) { throw 'Pivot refresh failed.' }
    [void]$pivotSheet.Columns.Item('A:F').AutoFit()
    [void]$book.Worksheets.Item('Read me').Activate()
    $explorer.Range('B2').Value2 = 'California statewide'
    $excel.CalculateFullRebuild()
    Assert-Near $pivot.GetPivotData('Published FTES','district','California statewide','fiscal_year','2024-25').Value2 $state.ftes 'Pivot statewide'
    Assert-Near $pivot.GetPivotData('Published FTES','district','Allan Hancock','fiscal_year','2024-25').Value2 $district.ftes 'Pivot district'
    Assert-Near $explorer.Range('B9').Value2 $state.ftes 'Explorer statewide'
    Assert-Near $explorer.Range('C9').Value2 $state.yoy_rate 'Explorer statewide change'
    $explorer.Range('B2').Value2 = 'Allan Hancock'
    $excel.CalculateFullRebuild()
    Assert-Near $explorer.Range('B9').Value2 $district.ftes 'Explorer district'
    Assert-Near $explorer.Range('C9').Value2 $district.yoy_rate 'Explorer district change'
    $explorer.Range('B2').Value2 = 'California statewide'
    $excel.CalculateFullRebuild()
    $book.Save()
    Write-Output "Excel $($excel.Version): native public FTES PivotTable refreshed; statewide and district figures reconciled; selector and YoY formulas recalculated."
} finally {
    if ($null -ne $book) { $book.Close($false) }
    $excel.Quit()
    [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($excel)
}
