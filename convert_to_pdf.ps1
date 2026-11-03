$docPath = "C:\Users\Shubham\NoSQLProject\NoSQL_Project_Report.docx"
$pdfPath = "C:\Users\Shubham\NoSQLProject\NoSQL_Project_Report.pdf"

try {
    Write-Host "Initializing Word Application COM object..."
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    
    Write-Host "Opening document: $docPath ..."
    $doc = $word.Documents.Open($docPath)
    
    Write-Host "Exporting as PDF: $pdfPath ..."
    # 17 = wdFormatPDF
    $doc.SaveAs([ref]$pdfPath, [ref]17)
    
    $doc.Close()
    $word.Quit()
    
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($doc) | Out-Null
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
    
    if (Test-Path $pdfPath) {
        $size = (Get-Item $pdfPath).Length
        Write-Host "SUCCESS: PDF created successfully at $pdfPath ($size bytes)"
    } else {
        Write-Host "ERROR: PDF file was not created."
    }
} catch {
    Write-Host "Error occurred during Word COM conversion: $_"
}
