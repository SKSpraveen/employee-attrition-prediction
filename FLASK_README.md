# Flask Web Frontend for Employee Attrition Prediction

## Quick Start - Step by Step

### ✨ Option 1: ONE-CLICK Run (Easiest - Windows Users)

**Step 1:** Find the file `run_app.bat` in your project folder
- Location: `employee-attrition-prediction\run_app.bat`

**Step 2:** Double-click the `run_app.bat` file
- This will automatically open PowerShell and start the Flask server

**Step 3:** Wait for the message to appear
- You should see: `Running on http://127.0.0.1:5000`

**Step 4:** Open your browser
- Type in address bar: `http://127.0.0.1:5000`
- Or click the link if it appears in terminal

**Done! 🎉** You can now upload employee data and get predictions


---

### 📋 Option 2: Manual Setup (Step-by-Step Instructions)

#### **Step 1: Open PowerShell**
- Right-click on your project folder: `employee-attrition-prediction`
- Select: **"Open PowerShell window here"** (or **"Open in Terminal"** in Windows 11)
- You should see a blue terminal window

#### **Step 2: Check if virtual environment exists**
```powershell
ls -Name | findstr venv
```
**Expected output:** You should see `.venv` or `venv` listed

#### **Step 3: Activate the virtual environment**
If you see `.venv` in the folder:
```powershell
.\.venv\Scripts\Activate.ps1
```

If you see `venv` in the folder:
```powershell
.\venv\Scripts\Activate.ps1
```

**Expected output:** Your terminal will show `(venv)` or `(.venv)` at the beginning of lines
```
(.venv) PS C:\Users\ASUS\Desktop\Campus\employee-attrition-prediction>
```

#### **Step 4: Install required packages (if not already installed)**
```powershell
pip install Flask pandas scikit-learn xgboost joblib
```

**What this does:** Downloads and installs all required libraries
**Wait time:** 2-5 minutes (first time only)

**Expected output:** Lines saying `Successfully installed...`

#### **Step 5: Navigate to the app folder**
```powershell
cd app
```

**Expected output:** Your path changes to:
```
(.venv) PS C:\Users\ASUS\Desktop\Campus\employee-attrition-prediction\app>
```

#### **Step 6: Start the Flask application**
```powershell
python app.py
```

**Expected output:** You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
 * Press CTRL+C to quit
```

#### **Step 7: Open your browser**
- Open any browser (Chrome, Edge, Firefox, etc.)
- Go to address bar and type: `http://127.0.0.1:5000`
- Press Enter

**Done! 🎉** The web app is now running locally

---

## 🎯 Features - What You Can Do

1. **Upload Employee Data**
   - Click "Choose File" and select your CSV file
   - CSV should contain employee information (Age, Salary, Department, etc.)

2. **Select a Prediction Model**
   - **Random Forest** - Catches more at-risk employees (better for prevention)
   - **XGBoost** - Best balanced performance (⭐ Recommended)
   - **SVM** - Most accurate with fewer false alarms
   - **KNN** - Simple baseline model

3. **Get Instant Predictions**
   - See which employees are at risk of leaving
   - View prediction confidence scores
   - Download results in table format

4. **View Model Comparison**
   - Click "Compare Models" to see performance metrics
   - See accuracy, precision, recall for all 4 models
   - Get HR team recommendations on which model to use

---

## 📊 Input CSV Format

Your CSV file should have these columns:
```
Age, Department, Salary, Years_With_Company, 
Monthly_Income, Overtime, Job_Satisfaction, 
And other HR-related features...
```

**Important:** The CSV must have the SAME column names and features that were used to train the models.

**Example:** 
```
Age,Department,Salary,MonthlyIncome,YearsAtCompany,Overtime,JobSatisfaction
28,Sales,65000,5417,2,Yes,3
35,IT,85000,7083,5,No,4
42,HR,72000,6000,8,Yes,2
```

---

## 🆘 Troubleshooting

### Problem: "Flask not found" error
```
ModuleNotFoundError: No module named 'flask'
```
**Solution:** Make sure virtual environment is activated (you should see `.venv` in brackets)
Then run:
```powershell
pip install Flask pandas scikit-learn xgboost joblib
```

### Problem: "Model file not found" error
```
FileNotFoundError: [Errno 2] No such file or directory: '...random_forest_best_model.pkl'
```
**Solution:** 
- Make sure you're running from inside the `app` folder
- Check that model files exist in `outputs/models/` folder
- Verify paths in [app.py line 12-17](../app/app.py#L12-L17)

### Problem: "Port 5000 in use" error
```
OSError: [Errno 10048] Address already in use
```
**Solution:** Another application is using port 5000
- **Option A:** Close the other app
- **Option B:** Change port in `app.py` line 163 from `port=5000` to `port=5001`
  ```python
  app.run(debug=True, host='127.0.0.1', port=5001)
  ```
- Then access: `http://127.0.0.1:5001`

### Problem: "Cannot activate virtual environment"
```
PowerShell: File .\.venv\Scripts\Activate.ps1 cannot be loaded
```
**Solution:** Your PowerShell execution policy is restricted
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then try activation again

### Problem: Flask starts but "Connection refused" when opening browser
**Solution:** 
- Wait 5-10 seconds after Flask starts
- Make sure you copy the correct URL from terminal
- Try opening: `http://localhost:5000` instead of `127.0.0.1:5000`

---

## 📁 File Structure
## 📁 File Structure

```
employee-attrition-prediction/
│
├── 📄 FLASK_README.md                    ← You are here!
├── 📄 run_app.bat                        ← One-click startup (Windows)
│
├── 📂 app/
│   ├── 📄 app.py                         ← Main Flask application  
│   ├── 📂 templates/
│   │   ├── index.html                    ← Home page (upload & predictions)
│   │   └── compare.html                  ← Model comparison dashboard
│   └── 📂 static/
│       └── style.css                     ← Styling
│
├── 📂 outputs/
│   ├── 📂 models/
│   │   ├── random_forest_best_model.pkl
│   │   ├── xgboost_attrition_model.joblib
│   │   └── knn_best_model.joblib
│   │
│   ├── 📂 SVM/
│   │   └── best_svm_model.joblib
│   │
│   └── 📂 metrics/
│       └── (performance metrics)
│
├── 📂 notebooks/
│   └── (training notebooks for each model)
│
└── 📂 .venv/
    └── (virtual environment - Python packages)
```

---

## 🤔 Understanding the Web App Flow

```
You Upload CSV File
         ↓
    Flask Backend (app.py)
    - Loads the selected ML model
    - Processes your data
    - Makes predictions
         ↓
    Results Displayed
    - Table with predictions (Red = At Risk, Green = Safe)
    - Charts showing attrition breakdown
    - Model accuracy info
    - HR team recommendations
```

---

## 📱 Accessing the App on Other Devices

### From Same Computer (Current Setup)
- URL: `http://127.0.0.1:5000` or `http://localhost:5000`

### From Another Computer on Same WiFi Network
1. Find your computer's IP address:
   ```powershell
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., `192.168.x.x`)

2. On another computer, open browser and go to:
   ```
   http://YOUR_IP_ADDRESS:5000
   ```
   Example: `http://192.168.1.105:5000`

3. Note: This only works if both computers are on the same WiFi network

### For Internet Access (Not Local Network)
- Need to deploy to cloud service (Heroku, AWS, Azure)
- Or use ngrok tunnel (advanced)

---

## 💾 Saving Your Work

After you're done predicting:
1. Results are displayed on the web page
2. You can **right-click → Save As** to save the page
3. Or **Ctrl+P** to print/save as PDF

---

## 🛑 How to Stop the App

1. Go to PowerShell terminal where app is running
2. Press: **`Ctrl + C`**
3. You'll see: `KeyboardInterrupt` - this means app stopped
4. Terminal is now safe to close

---

## ⚙️ Advanced: Change Flask Settings

Edit [app.py lines 162-163](app/app.py#L162-L163):

```python
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
    #       ↑              ↑                    ↑
    #    Debug mode    Who can access      Port number
```

Options:
- `debug=False` - Turn off auto-reload (faster)
- `host='0.0.0.0'` - Allow all computers to connect (less secure)
- `port=5001` - Use different port number

---

## ✅ Checklist: Am I Ready?

- [ ] Python installed (`python --version` returns version number)
- [ ] Virtual environment activated (you see `.venv` or `venv` in brackets)
- [ ] All packages installed (ran `pip install...`)
- [ ] Inside `app` folder (`cd app`)
- [ ] Ran `python app.py` command
- [ ] See "Running on http://127.0.0.1:5000" message
- [ ] Browser shows the home page when I visit the URL

**If all checked ✅** - You're ready to use the app!

---

## 📞 Common Questions

**Q: Do I need internet to run this?**
A: No, it runs completely offline. Internet is optional.

**Q: Can multiple people use it at the same time?**
A: Yes, if you use `host='0.0.0.0'` and share your IP address.

**Q: How long does a prediction take?**
A: Usually instant (< 1 second) for small datasets.

**Q: Where are my predictions saved?**
A: On the web page. You can screenshot or print-to-PDF to save.

**Q: What if I get an error I can't fix?**
A: Check the troubleshooting section above, or check PowerShell for error details.
