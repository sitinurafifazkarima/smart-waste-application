# 🚀 SCRIPT UNTUK MENJALANKAN SMART WASTE CLASSIFIER
# Simpan file ini sebagai: run_app.ps1
# Cara menjalankan: Klik kanan > Run with PowerShell
# Atau di terminal: .\run_app.ps1

Write-Host ""
Write-Host "=================================" -ForegroundColor Green
Write-Host "  SMART WASTE CLASSIFIER v1.0   " -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host ""

# Cek apakah di folder yang benar
$currentDir = Get-Location
$expectedPath = "app_pilahsampah"

if ($currentDir.Path -notlike "*$expectedPath*") {
    Write-Host "⚠️  Warning: Anda tidak berada di folder app_pilahsampah" -ForegroundColor Yellow
    Write-Host "   Pindah ke folder yang benar..." -ForegroundColor Yellow
    
    $appPath = "d:\Materi KIR SMPITIK\app_pilahsampah"
    
    if (Test-Path $appPath) {
        Set-Location $appPath
        Write-Host "✅ Berhasil pindah ke: $appPath" -ForegroundColor Green
    } else {
        Write-Host "❌ Error: Folder tidak ditemukan!" -ForegroundColor Red
        Write-Host "   Pastikan path benar di line 19 script ini" -ForegroundColor Red
        Read-Host "Tekan Enter untuk keluar"
        exit
    }
}

Write-Host "📂 Lokasi aplikasi: $(Get-Location)" -ForegroundColor Cyan
Write-Host ""

# Cek apakah Python terinstall
Write-Host "🔍 Mengecek Python..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python terdeteksi: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python tidak ditemukan!" -ForegroundColor Red
    Write-Host "   Install Python dari: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Tekan Enter untuk keluar"
    exit
}

Write-Host ""

# Cek apakah requirements sudah terinstall
Write-Host "🔍 Mengecek dependencies..." -ForegroundColor Cyan

$checkStreamlit = python -c "import streamlit" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Dependencies belum terinstall" -ForegroundColor Yellow
    Write-Host ""
    $install = Read-Host "Install sekarang? (Y/N)"
    
    if ($install -eq "Y" -or $install -eq "y") {
        Write-Host ""
        Write-Host "📦 Installing dependencies..." -ForegroundColor Cyan
        Write-Host "   (Ini mungkin memakan waktu beberapa menit...)" -ForegroundColor Yellow
        Write-Host ""
        
        pip install -r requirements.txt
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "✅ Dependencies berhasil diinstall!" -ForegroundColor Green
        } else {
            Write-Host ""
            Write-Host "❌ Error saat install dependencies" -ForegroundColor Red
            Read-Host "Tekan Enter untuk keluar"
            exit
        }
    } else {
        Write-Host "❌ Aplikasi tidak dapat berjalan tanpa dependencies" -ForegroundColor Red
        Write-Host "   Jalankan: pip install -r requirements.txt" -ForegroundColor Yellow
        Read-Host "Tekan Enter untuk keluar"
        exit
    }
} else {
    Write-Host "✅ Dependencies sudah terinstall" -ForegroundColor Green
}

Write-Host ""
Write-Host "=================================" -ForegroundColor Green
Write-Host "  🚀 MEMULAI APLIKASI...        " -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host ""
Write-Host "📌 Aplikasi akan terbuka di browser" -ForegroundColor Cyan
Write-Host "📌 URL: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️  Jangan tutup window ini selama aplikasi berjalan!" -ForegroundColor Yellow
Write-Host "⚠️  Untuk stop aplikasi: Tekan Ctrl+C" -ForegroundColor Yellow
Write-Host ""
Write-Host "=================================" -ForegroundColor Green
Write-Host ""

# Jalankan aplikasi
streamlit run app.py

# Jika aplikasi ditutup
Write-Host ""
Write-Host "=================================" -ForegroundColor Yellow
Write-Host "  Aplikasi telah ditutup        " -ForegroundColor Yellow
Write-Host "=================================" -ForegroundColor Yellow
Write-Host ""
Read-Host "Tekan Enter untuk keluar"
