# CLV 顧客終身價值專題網站

靜態網站，可直接放到 GitHub Pages。

## 上線步驟
1. 在 GitHub 建一個新的 public repository（例如 `CLV_analysis`）。
2. 把這個資料夾裡的所有檔案（含 `img` 資料夾）上傳到 repository 根目錄。
3. Settings → Pages → Source 選 `Deploy from a branch`，Branch 選 `main`、資料夾 `/ (root)`，按 Save。
4. 約 1～2 分鐘後，網址會是 `https://你的帳號.github.io/CLV_analysis/`。

## 成果展示頁的按鈕
Streamlit 系統部署到 Streamlit Community Cloud 後，打開 `demo.html`，
把「線上系統網址尚未設定」那個按鈕改成：
`<a class="btn" href="你的 Streamlit 網址" target="_blank" rel="noopener">開啟 CLV 顧客價值分析系統 →</a>`
