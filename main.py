
# from fastapi import FastAPI, Form, Request, HTTPException, Depends
# from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
# from fastapi.security import HTTPBasic, HTTPBasicCredentials
# import gspread
# from google.oauth2.service_account import Credentials
# from datetime import datetime
# import calendar
# from unidecode import unidecode
# import secrets
# import os
# import json
# import asyncio
# from functools import lru_cache
# from typing import List, Optional

# app = FastAPI()
# security = HTTPBasic()

# # Auth credentials
# VALID_USERNAME = "MarketingPFL"
# VALID_PASSWORD = "yordamkerak"

# def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
#     is_correct_username = secrets.compare_digest(credentials.username, VALID_USERNAME)
#     is_correct_password = secrets.compare_digest(credentials.password, VALID_PASSWORD)
#     if not (is_correct_username and is_correct_password):
#         raise HTTPException(
#             status_code=401,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Basic"},
#         )
#     return credentials.username

# def get_google_credentials():
#     try:
#         creds_path = "credentials.json"
#         SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#         creds = Credentials.from_service_account_file(creds_path, scopes=SCOPE)
#         return gspread.authorize(creds)
#     except Exception as e:
#         print(f"Error getting credentials: {e}")
#         return None

# # Global variables with caching
# client = None
# _cached_data = None

# # @lru_cache(maxsize=1)
# def get_cached_sheets_data():
#     global client, _cached_data
#     try:
#         if not client:
#             client = get_google_credentials()
        
#         if client and not _cached_data:
#             SPREADSHEET_NAME = "DoriXarajatlar"
#             spreadsheet = client.open(SPREADSHEET_NAME)
            
#             shifokorlar_sheet = spreadsheet.worksheet("Shifokorlar")
#             dorixonalar_sheet = spreadsheet.worksheet("Dorixonalar")
#             ismlar_sheet = spreadsheet.worksheet("IsmFamiliya")
#             regionlar_sheet = spreadsheet.worksheet("Regionlar")
            
#             shifokorlar = shifokorlar_sheet.col_values(1)[1:]
#             dorixonalar = dorixonalar_sheet.col_values(1)[1:]
#             ismlar = ismlar_sheet.col_values(1)[1:]
#             regionlar = regionlar_sheet.col_values(1)[1:]
            
#             _cached_data = {
#                 'shifokorlar': shifokorlar,
#                 'dorixonalar': dorixonalar,
#                 'ismlar': ismlar,
#                 'regionlar': regionlar
#             }
            
#         return _cached_data
#     except Exception as e:
#         print(f"Error getting cached data: {e}")
#         return None

# def get_recommendations_fast(user_input: str, options: List[str], limit: int = 10) -> List[str]:
#     if not user_input or len(user_input) < 1:
#         return []
    
#     user_input_norm = unidecode(user_input).lower()
#     matches = []
    
#     for opt in options:
#         opt_norm = unidecode(opt).lower()
#         if user_input_norm == opt_norm:
#             return [opt]
#         elif user_input_norm in opt_norm:
#             score = len(user_input_norm) / len(opt_norm)
#             matches.append((opt, score))
            
#             if len(matches) >= limit * 2:
#                 break
    
#     matches.sort(key=lambda x: x[1], reverse=True)
#     return [match[0] for match in matches[:limit]]

# @app.on_event("startup")
# async def startup_event():
#     print("Initializing data...")
#     data = get_cached_sheets_data()
#     if data:
#         print("✅ Data loaded successfully")
#     else:
#         print("⚠️ Warning: Could not initialize Google Sheets")

# @app.get("/", response_class=HTMLResponse)
# async def main_page(request: Request, username: str = Depends(authenticate)):
#     html_content = """
#     <!DOCTYPE html>
#     <html lang="uz">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>💊 Дори харажатлари</title>
#         <style>
#             * { margin: 0; padding: 0; box-sizing: border-box; }
            
#             body {
#                 font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
#                 background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#                 min-height: 100vh;
#                 padding: 10px;
#             }
            
#             .container {
#                 max-width: 1000px;
#                 margin: 0 auto;
#                 background: white;
#                 border-radius: 15px;
#                 box-shadow: 0 20px 40px rgba(0,0,0,0.1);
#                 overflow: hidden;
#                 position: relative;
#             }
            
#             .header {
#                 background: linear-gradient(45deg, #667eea, #764ba2);
#                 color: white;
#                 padding: 20px;
#                 text-align: center;
#                 position: relative;
#             }
            
#             .sidebar-toggle {
#                 position: absolute;
#                 top: 50%;
#                 left: 20px;
#                 transform: translateY(-50%);
#                 background: rgba(255,255,255,0.2);
#                 border: none;
#                 color: white;
#                 padding: 10px;
#                 border-radius: 8px;
#                 cursor: pointer;
#                 font-size: 18px;
#                 transition: background 0.2s;
#             }
            
#             .sidebar-toggle:hover {
#                 background: rgba(255,255,255,0.3);
#             }
            
#             .sidebar {
#                 position: fixed;
#                 top: 0;
#                 left: -300px;
#                 width: 300px;
#                 height: 100vh;
#                 background: white;
#                 box-shadow: 2px 0 10px rgba(0,0,0,0.1);
#                 transition: left 0.3s ease;
#                 z-index: 2000;
#                 padding: 20px;
#             }
            
#             .sidebar.active {
#                 left: 0;
#             }
            
#             .sidebar-header {
#                 padding-bottom: 20px;
#                 border-bottom: 1px solid #eee;
#                 margin-bottom: 20px;
#             }
            
#             .sidebar-close {
#                 float: right;
#                 background: none;
#                 border: none;
#                 font-size: 24px;
#                 cursor: pointer;
#                 color: #666;
#             }
            
#             .sidebar-menu {
#                 list-style: none;
#             }
            
#             .sidebar-menu li {
#                 margin-bottom: 10px;
#             }
            
#             .sidebar-menu a {
#                 display: block;
#                 padding: 15px;
#                 text-decoration: none;
#                 color: #333;
#                 border-radius: 8px;
#                 transition: all 0.2s;
#             }
            
#             .sidebar-menu a:hover, .sidebar-menu a.active {
#                 background: #f8f9fa;
#                 color: #667eea;
#             }
            
#             .overlay {
#                 position: fixed;
#                 top: 0;
#                 left: 0;
#                 width: 100vw;
#                 height: 100vh;
#                 background: rgba(0,0,0,0.5);
#                 z-index: 1500;
#                 display: none;
#             }
            
#             .overlay.active {
#                 display: block;
#             }
            
#             .content {
#                 padding: 30px;
#             }
            
#             .section {
#                 display: none;
#             }
            
#             .section.active {
#                 display: block;
#             }
            
#             .form-row {
#                 display: flex;
#                 gap: 15px;
#                 margin-bottom: 20px;
#                 flex-wrap: wrap;
#             }
            
#             .form-group {
#                 position: relative;
#                 flex: 1;
#                 min-width: 250px;
#             }
            
#             .form-group.full-width {
#                 flex: 100%;
#                 min-width: 100%;
#             }
            
#             label {
#                 display: block;
#                 margin-bottom: 8px;
#                 font-weight: 600;
#                 color: #333;
#                 font-size: 14px;
#             }
            
#             .required { color: #e74c3c; }
            
#             input, select, textarea {
#                 width: 100%;
#                 padding: 12px;
#                 border: 2px solid #e1e5e9;
#                 border-radius: 8px;
#                 font-size: 16px;
#                 transition: border-color 0.2s;
#                 background-color: #fff;
#             }
            
#             /* Editable select styles */
#             select[data-editable="true"] {
#                 background: white url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="12" height="8" viewBox="0 0 12 8"><path fill="%23666" d="M6 8L0 2h12z"/></svg>') no-repeat right 12px center;
#                 appearance: none;
#                 -webkit-appearance: none;
#                 -moz-appearance: none;
#             }
            
#             input:focus, select:focus, textarea:focus {
#                 outline: none;
#                 border-color: #667eea;
#                 box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
#             }
            
#             .suggestions {
#                 position: absolute;
#                 top: 100%;
#                 left: 0;
#                 right: 0;
#                 background: white;
#                 border: 1px solid #e1e5e9;
#                 border-top: none;
#                 border-radius: 0 0 8px 8px;
#                 max-height: 200px;
#                 overflow-y: auto;
#                 z-index: 1000;
#                 box-shadow: 0 4px 15px rgba(0,0,0,0.15);
#                 display: none;
#             }
            
#             .suggestion-item {
#                 padding: 12px;
#                 cursor: pointer;
#                 border-bottom: 1px solid #f1f1f1;
#                 transition: background-color 0.15s;
#             }
            
#             .suggestion-item:hover, .suggestion-item.active {
#                 background-color: #f8f9fa;
#             }
            
#             .suggestion-item:last-child { border-bottom: none; }
            
#             .btn {
#                 background: linear-gradient(45deg, #667eea, #764ba2);
#                 color: white;
#                 padding: 15px 30px;
#                 border: none;
#                 border-radius: 8px;
#                 font-size: 16px;
#                 cursor: pointer;
#                 transition: all 0.2s;
#                 font-weight: 600;
#                 min-width: 150px;
#             }
            
#             .btn:hover {
#                 transform: translateY(-2px);
#                 box-shadow: 0 5px 15px rgba(102,126,234,0.4);
#             }
            
#             .btn:active { transform: translateY(0); }
            
#             .btn:disabled {
#                 opacity: 0.6;
#                 cursor: not-allowed;
#                 transform: none;
#             }
            
#             .btn-secondary {
#                 background: linear-gradient(45deg, #28a745, #20c997);
#             }
            
#             .btn-secondary:hover {
#                 box-shadow: 0 5px 15px rgba(40,167,69,0.4);
#             }
            
#             .message {
#                 padding: 15px;
#                 margin: 15px 0;
#                 border-radius: 8px;
#                 font-weight: 500;
#                 display: none;
#             }
            
#             .success {
#                 background: #d4edda;
#                 color: #155724;
#                 border-left: 4px solid #28a745;
#             }
            
#             .error {
#                 background: #f8d7da;
#                 color: #721c24;
#                 border-left: 4px solid #dc3545;
#             }
            
#             .loading {
#                 display: none;
#                 text-align: center;
#                 padding: 20px;
#             }
            
#             .spinner {
#                 border: 3px solid #f3f3f3;
#                 border-top: 3px solid #667eea;
#                 border-radius: 50%;
#                 width: 30px;
#                 height: 30px;
#                 animation: spin 1s linear infinite;
#                 margin: 0 auto 10px;
#             }
            
#             @keyframes spin {
#                 0% { transform: rotate(0deg); }
#                 100% { transform: rotate(360deg); }
#             }
            
#             .legend {
#                 background: #f8f9fa;
#                 padding: 15px;
#                 border-radius: 8px;
#                 margin-top: 20px;
#                 text-align: center;
#                 color: #666;
#                 font-size: 14px;
#             }
            
#             .search-indicator {
#                 position: absolute;
#                 right: 12px;
#                 top: 50%;
#                 transform: translateY(-50%);
#                 color: #666;
#                 font-size: 12px;
#                 display: none;
#             }
            
#             /* Mobile Responsive */
#             @media (max-width: 768px) {
#                 body {
#                     padding: 5px;
#                 }
                
#                 .container {
#                     border-radius: 10px;
#                 }
                
#                 .header {
#                     padding: 15px;
#                 }
                
#                 .header h1 {
#                     font-size: 20px;
#                     margin-top: 10px;
#                 }
                
#                 .content {
#                     padding: 15px;
#                 }
                
#                 .form-row {
#                     flex-direction: column;
#                     gap: 10px;
#                 }
                
#                 .form-group {
#                     min-width: 100%;
#                 }
                
#                 input, select, textarea {
#                     font-size: 16px; /* Prevents zoom on iOS */
#                     padding: 15px 12px;
#                 }
                
#                 .btn {
#                     width: 100%;
#                     padding: 18px;
#                     font-size: 18px;
#                 }
                
#                 .sidebar {
#                     width: 280px;
#                 }
                
#                 .sidebar-toggle {
#                     left: 15px;
#                     padding: 8px;
#                 }
#             }
            
#             @media (max-width: 480px) {
#                 .header h1 {
#                     font-size: 18px;
#                 }
                
#                 .content {
#                     padding: 10px;
#                 }
                
#                 .sidebar {
#                     width: 100%;
#                     left: -100%;
#                 }
#             }
#         </style>
#     </head>
#     <body>
#         <!-- Sidebar -->
#         <div id="sidebar" class="sidebar">
#             <div class="sidebar-header">
#                 <h3>📋 Меню</h3>
#                 <button class="sidebar-close" onclick="toggleSidebar()">×</button>
#             </div>
#             <ul class="sidebar-menu">
#                 <li><a href="#" class="menu-item active" data-section="main-form">📊 Асосий форма</a></li>
#                 <li><a href="#" class="menu-item" data-section="add-doctor">👨‍⚕️ Янги врач қўшиш</a></li>
#             </ul>
#         </div>
        
#         <div id="overlay" class="overlay" onclick="toggleSidebar()"></div>
        
#         <div class="container">
#             <div class="header">
#                 <button class="sidebar-toggle" onclick="toggleSidebar()">☰</button>
#                 <h1>💊 Маркетинг учун рўйхат</h1>
#             </div>
            
#             <div class="content">
#                 <!-- Main Form Section -->
#                 <div id="main-form" class="section active">
#                     <form id="mainForm">
#                         <div class="form-row">
#                             <div class="form-group">
#                                 <label for="ism">👤 Исм-Фамилия <span class="required">*</span></label>
#                                 <select id="ism" name="ism" required data-editable="true">
#                                     <option value="">Танланг ёки киритинг...</option>
#                                 </select>
#                             </div>
#                             <div class="form-group">
#                                 <label for="region">📍 Регион <span class="required">*</span></label>
#                                 <select id="region" name="region" required>
#                                     <option value="">Танланг...</option>
#                                 </select>
#                             </div>
#                         </div>

#                         <div class="form-row">
#                             <div class="form-group">
#                                 <label for="vrach">👨‍⚕️ Врач <span class="required">*</span></label>
#                                 <input type="text" id="vrach" name="vrach" required autocomplete="off" 
#                                        placeholder="Врач номини киритинг...">
#                                 <div class="search-indicator" id="vrach-indicator">🔍</div>
#                                 <div id="vrach-suggestions" class="suggestions"></div>
#                             </div>
#                             <div class="form-group">
#                                 <label for="harajat_turi">💼 Инвеститция тури <span class="required">*</span></label>
#                                 <select id="harajat_turi" name="harajat_turi" required>
#                                     <option value="">Танланг...</option>
#                                     <option value="Аптека 100%">Аптека 100%</option>
#                                     <option value="Оптовик маркетинг 23%">Оптовик маркетинг 23%</option>
#                                     <option value="Предоплата маркетинг">Предоплата маркетинг</option>
#                                     <option value="Аванс маркетинг">Аванс маркетинг</option>
#                                 </select>
#                             </div>
#                         </div>

#                         <div class="form-row">
#                             <div class="form-group">
#                                 <label for="apteka">🏥 Аптека <span class="required">*</span></label>
#                                 <input type="text" id="apteka" name="apteka" required autocomplete="off"
#                                        placeholder="Аптека номини киритинг...">
#                                 <div class="search-indicator" id="apteka-indicator">🔍</div>
#                                 <div id="apteka-suggestions" class="suggestions"></div>
#                             </div>
#                             <div class="form-group">
#                                 <label for="summa_bonus">💰 Сумма бонус <span class="required">*</span></label>
#                                 <input type="number" id="summa_bonus" name="summa_bonus" step="0.01" 
#                                        min="0.01" required placeholder="0.00">
#                             </div>
#                         </div>

#                         <div class="form-row">
#                             <div class="form-group">
#                                 <label for="kompaniya_turi">🏢 Бренд <span class="required">*</span></label>
#                                 <select id="kompaniya_turi" name="kompaniya_turi" required>
#                                     <option value="">Танланг...</option>
#                                     <option value="GMX">GMX</option>
#                                     <option value="BP">BP</option>
#                                 </select>
#                             </div>
#                             <div class="form-group">
#                                 <label for="izoh">📝 Изоҳ <span class="required">*</span></label>
#                                 <textarea id="izoh" name="izoh" rows="3" required 
#                                           placeholder="Изоҳ киритинг..."></textarea>
#                             </div>
#                         </div>

#                         <div style="text-align: center; margin-top: 30px;">
#                             <button type="submit" class="btn" id="submitBtn">
#                                 ✅ Сақлаш
#                             </button>
#                         </div>
#                     </form>
#                 </div>
                
#                 <!-- Add Doctor Section -->
#                 <div id="add-doctor" class="section">
#                     <h2>👨‍⚕️ Янги врач қўшиш</h2>
#                     <form id="doctorForm">
#                         <div class="form-row">
#                             <div class="form-group">
#                                 <label for="doctor_region">📍 Регион <span class="required">*</span></label>
#                                 <select id="doctor_region" name="doctor_region" required>
#                                     <option value="">Танланг...</option>
#                                 </select>
#                             </div>
#                             <div class="form-group">
#                                 <label for="doctor_mp">👤 МП <span class="required">*</span></label>
#                                 <select id="doctor_mp" name="doctor_mp" required data-editable="true">
#                                     <option value="">Танланг ёки киритинг...</option>
#                                 </select>
#                             </div>
#                         </div>
                        
#                         <div class="form-row">
#                             <div class="form-group">
#                                 <label for="dori_nomi">💊 Дори номи <span class="required">*</span></label>
#                                 <input type="text" id="dori_nomi" name="dori_nomi" required 
#                                        placeholder="Дори номини киритинг...">
#                             </div>
#                             <div class="form-group">
#                                 <label for="lpu">🏥 ЛПУ <span class="required">*</span></label>
#                                 <input type="text" id="lpu" name="lpu" required 
#                                        placeholder="ЛПУ номини киритинг...">
#                             </div>
#                         </div>
                        
#                         <div class="form-row">
#                             <div class="form-group">
#                                 <label for="mutaxasislik">🩺 Мутахассислик <span class="required">*</span></label>
#                                 <input type="text" id="mutaxasislik" name="mutaxasislik" required 
#                                        placeholder="Мутахассислик киритинг...">
#                             </div>
#                             <div class="form-group">
#                                 <label for="tel_no">📞 Телефон рақами <span class="required">*</span></label>
#                                 <input type="tel" id="tel_no" name="tel_no" required 
#                                        placeholder="+998901234567">
#                             </div>
#                         </div>
                        
#                         <div class="form-row">
#                             <div class="form-group full-width">
#                                 <label for="doctor_name">👨‍⚕️ Врач исм-фамилияси <span class="required">*</span></label>
#                                 <input type="text" id="doctor_name" name="doctor_name" required 
#                                        placeholder="Исм-фамилия киритинг...">
#                             </div>
#                         </div>
                        
#                         <div style="text-align: center; margin-top: 30px;">
#                             <button type="submit" class="btn btn-secondary" id="doctorSubmitBtn">
#                                 ➕ Врач қўшиш
#                             </button>
#                         </div>
#                     </form>
#                 </div>
                
#                 <div id="loading" class="loading">
#                     <div class="spinner"></div>
#                     <p>Юкланмоқда...</p>
#                 </div>
                
#                 <div id="message" class="message"></div>
                
#                 <div class="legend">
#                     <span class="required">*</span> - Мажбурий майдонлар
#                 </div>
#             </div>
#         </div>
        
#         <script>
#         // Global variables
#         let debounceTimers = {};
#         let cachedData = { doctors: [], pharmacies: [], names: [], regions: [] };
        
#         const elements = {
#             ism: null, region: null, vrach: null, apteka: null,
#             doctorRegion: null, doctorMp: null,
#             vrachSuggestions: null, aptekaSuggestions: null,
#             vrachIndicator: null, aptekaIndicator: null,
#             form: null, doctorForm: null, message: null, loading: null,
#             submitBtn: null, doctorSubmitBtn: null
#         };
        
#         // Initialize
#         document.addEventListener('DOMContentLoaded', function() {
#             cacheElements();
#             initializeData();
#             setupEventListeners();
#             setupEditableSelects();
#         });
        
#         function cacheElements() {
#             elements.ism = document.getElementById('ism');
#             elements.region = document.getElementById('region');
#             elements.vrach = document.getElementById('vrach');
#             elements.apteka = document.getElementById('apteka');
#             elements.doctorRegion = document.getElementById('doctor_region');
#             elements.doctorMp = document.getElementById('doctor_mp');
#             elements.vrachSuggestions = document.getElementById('vrach-suggestions');
#             elements.aptekaSuggestions = document.getElementById('apteka-suggestions');
#             elements.vrachIndicator = document.getElementById('vrach-indicator');
#             elements.aptekaIndicator = document.getElementById('apteka-indicator');
#             elements.form = document.getElementById('mainForm');
#             elements.doctorForm = document.getElementById('doctorForm');
#             elements.message = document.getElementById('message');
#             elements.loading = document.getElementById('loading');
#             elements.submitBtn = document.getElementById('submitBtn');
#             elements.doctorSubmitBtn = document.getElementById('doctorSubmitBtn');
#         }
        
#         async function initializeData() {
#             try {
#                 await Promise.all([loadNames(), loadRegions()]);
#                 console.log('✅ Data loaded successfully');
#             } catch (error) {
#                 console.error('❌ Error loading data:', error);
#                 showMessage('Маълумотлар юклашда хатолик юз берди', 'error');
#             }
#         }
        
#         async function loadNames() {
#             const response = await fetch('/get_names/');
#             const data = await response.json();
#             cachedData.names = data.names;
            
#             // Load names for main form
#             const fragment1 = document.createDocumentFragment();
#             data.names.forEach(name => {
#                 const option = document.createElement('option');
#                 option.value = name;
#                 option.textContent = name;
#                 fragment1.appendChild(option);
#             });
#             elements.ism.appendChild(fragment1);
            
#             // Load names for MP dropdown in doctor form
#             const fragment2 = document.createDocumentFragment();
#             data.names.forEach(name => {
#                 const option = document.createElement('option');
#                 option.value = name;
#                 option.textContent = name;
#                 fragment2.appendChild(option);
#             });
#             elements.doctorMp.appendChild(fragment2);
#         }
        
#         async function loadRegions() {
#             const response = await fetch('/get_regions/');
#             const data = await response.json();
#             cachedData.regions = data.regions;
            
#             // Load regions for main form
#             const fragment1 = document.createDocumentFragment();
#             data.regions.forEach(region => {
#                 const option = document.createElement('option');
#                 option.value = region;
#                 option.textContent = region;
#                 fragment1.appendChild(option);
#             });
#             elements.region.appendChild(fragment1);
            
#             // Load regions for doctor form
#             const fragment2 = document.createDocumentFragment();
#             data.regions.forEach(region => {
#                 const option = document.createElement('option');
#                 option.value = region;
#                 option.textContent = region;
#                 fragment2.appendChild(option);
#             });
#             elements.doctorRegion.appendChild(fragment2);
#         }
        
#         function setupEditableSelects() {
#             // Make selects with data-editable="true" behave like editable dropdowns
#             document.querySelectorAll('select[data-editable="true"]').forEach(select => {
#                 // Create hidden input for custom values
#                 const hiddenInput = document.createElement('input');
#                 hiddenInput.type = 'hidden';
#                 hiddenInput.name = select.name;
#                 select.parentNode.insertBefore(hiddenInput, select.nextSibling);
                
#                 // Handle select change
#                 select.addEventListener('change', function() {
#                     hiddenInput.value = this.value;
#                 });
                
#                 // Allow typing by converting to input-like behavior
#                 select.addEventListener('keydown', function(e) {
#                     if (e.key.length === 1) { // Single character key
#                         // Convert to searchable mode
#                         this.setAttribute('data-search-mode', 'true');
#                         this.style.color = '#666';
                        
#                         // Create a temporary option for search
#                         let searchOption = this.querySelector('option[data-search]');
#                         if (!searchOption) {
#                             searchOption = document.createElement('option');
#                             searchOption.setAttribute('data-search', 'true');
#                             searchOption.value = '';
#                             this.insertBefore(searchOption, this.firstChild);
#                         }
                        
#                         searchOption.textContent = e.key;
#                         searchOption.selected = true;
#                         hiddenInput.value = e.key;
                        
#                         // Prevent default select behavior
#                         e.preventDefault();
#                     }
#                 });
                
#                 // Handle further typing
#                 select.addEventListener('keyup', function(e) {
#                     if (this.getAttribute('data-search-mode') === 'true') {
#                         const searchOption = this.querySelector('option[data-search]');
#                         if (searchOption && e.key !== 'Backspace' && e.key !== 'Delete' && e.key.length === 1) {
#                             searchOption.textContent += e.key;
#                             hiddenInput.value = searchOption.textContent;
#                         } else if ((e.key === 'Backspace' || e.key === 'Delete') && searchOption) {
#                             let currentText = searchOption.textContent;
#                             if (currentText.length > 0) {
#                                 searchOption.textContent = currentText.slice(0, -1);
#                                 hiddenInput.value = searchOption.textContent;
#                             }
#                         }
#                     }
#                 });
                
#                 // Reset search mode on blur
#                 select.addEventListener('blur', function() {
#                     this.removeAttribute('data-search-mode');
#                     this.style.color = '';
#                     const searchOption = this.querySelector('option[data-search]');
#                     if (searchOption && searchOption.textContent.trim() === '') {
#                         searchOption.remove();
#                     }
#                 });
#             });
#         }
        
#         function setupEventListeners() {
#             // Search functionality
#             elements.vrach?.addEventListener('input', (e) => handleSearch(e, 'vrach'));
#             elements.apteka?.addEventListener('input', (e) => handleSearch(e, 'apteka'));
            
#             // Hide suggestions on outside click
#             document.addEventListener('click', (e) => {
#                 if (!e.target.closest('.form-group')) {
#                     hideSuggestions();
#                 }
#             });
            
#             // Form submissions
#             elements.form?.addEventListener('submit', handleMainFormSubmit);
#             elements.doctorForm?.addEventListener('submit', handleDoctorFormSubmit);
            
#             // Menu navigation
#             document.querySelectorAll('.menu-item').forEach(item => {
#                 item.addEventListener('click', (e) => {
#                     e.preventDefault();
#                     const section = e.target.dataset.section;
#                     showSection(section);
                    
#                     // Update active menu item
#                     document.querySelectorAll('.menu-item').forEach(mi => mi.classList.remove('active'));
#                     e.target.classList.add('active');
                    
#                     // Close sidebar on mobile
#                     if (window.innerWidth <= 768) {
#                         toggleSidebar();
#                     }
#                 });
#             });
#         }
        
#         function toggleSidebar() {
#             const sidebar = document.getElementById('sidebar');
#             const overlay = document.getElementById('overlay');
            
#             sidebar.classList.toggle('active');
#             overlay.classList.toggle('active');
#         }
        
#         function showSection(sectionId) {
#             document.querySelectorAll('.section').forEach(section => {
#                 section.classList.remove('active');
#             });
#             document.getElementById(sectionId).classList.add('active');
#         }
        
#         function handleSearch(e, type) {
#             const value = e.target.value;
#             const indicator = type === 'vrach' ? elements.vrachIndicator : elements.aptekaIndicator;
            
#             clearTimeout(debounceTimers[type]);
            
#             if (value.length >= 1) {
#                 indicator.style.display = 'block';
#                 debounceTimers[type] = setTimeout(() => {
#                     performSearch(value, type);
#                 }, 200);
#             } else {
#                 indicator.style.display = 'none';
#                 hideSuggestions(type);
#             }
#         }
        
#         async function performSearch(query, type) {
#             try {
#                 const endpoint = type === 'vrach' ? '/recommend_doctor/' : '/recommend_pharmacy/';
#                 const paramName = type === 'vrach' ? 'doctor_name' : 'pharmacy_name';
                
#                 const formData = new FormData();
#                 formData.append(paramName, query);
                
#                 const response = await fetch(endpoint, {
#                     method: 'POST',
#                     body: formData
#                 });
                
#                 const data = await response.json();
#                 displaySuggestions(type, data.recommendations);
                
#             } catch (error) {
#                 console.error(`Search error for ${type}:`, error);
#             } finally {
#                 const indicator = type === 'vrach' ? elements.vrachIndicator : elements.aptekaIndicator;
#                 indicator.style.display = 'none';
#             }
#         }
        
#         function displaySuggestions(type, suggestions) {
#             const container = type === 'vrach' ? elements.vrachSuggestions : elements.aptekaSuggestions;
#             const input = type === 'vrach' ? elements.vrach : elements.apteka;
            
#             container.innerHTML = '';
            
#             if (suggestions.length === 0) {
#                 container.style.display = 'none';
#                 return;
#             }
            
#             const fragment = document.createDocumentFragment();
#             suggestions.forEach(suggestion => {
#                 const div = document.createElement('div');
#                 div.className = 'suggestion-item';
#                 div.textContent = suggestion;
#                 div.addEventListener('click', () => {
#                     input.value = suggestion;
#                     hideSuggestions(type);
#                 });
#                 fragment.appendChild(div);
#             });
            
#             container.appendChild(fragment);
#             container.style.display = 'block';
#         }
        
#         function hideSuggestions(type) {
#             if (type) {
#                 const container = type === 'vrach' ? elements.vrachSuggestions : elements.aptekaSuggestions;
#                 container.style.display = 'none';
#             } else {
#                 elements.vrachSuggestions.style.display = 'none';
#                 elements.aptekaSuggestions.style.display = 'none';
#             }
#         }
        
#         // Main form submission
#         async function handleMainFormSubmit(e) {
#             e.preventDefault();
            
#             elements.submitBtn.disabled = true;
#             elements.submitBtn.textContent = '⏳ Сақланмоқда...';
            
#             showLoading(true);
#             hideMessage();
            
#             const formData = new FormData(elements.form);
            
#             // Handle editable selects
#             const ismHidden = document.querySelector('input[name="ism"]');
#             const regionHidden = document.querySelector('input[name="region"]');
            
#             if (ismHidden && ismHidden.value) {
#                 formData.set('ism', ismHidden.value);
#             }
#             if (regionHidden && regionHidden.value) {
#                 formData.set('region', regionHidden.value);
#             }
            
#             try {
#                 const response = await fetch('/save_data/', {
#                     method: 'POST',
#                     body: formData
#                 });
                
#                 const result = await response.json();
                
#                 if (result.success) {
#                     showMessage(result.message, 'success');
#                     elements.form.reset();
#                     elements.vrach.value = '';
#                     elements.apteka.value = '';
#                     hideSuggestions();
                    
#                     // Reset editable selects
#                     document.querySelectorAll('input[type="hidden"]').forEach(input => {
#                         input.value = '';
#                     });
#                 } else {
#                     showMessage(result.message, 'error');
#                 }
#             } catch (error) {
#                 showMessage('Хатолик юз берди: ' + error.message, 'error');
#             } finally {
#                 showLoading(false);
#                 elements.submitBtn.disabled = false;
#                 elements.submitBtn.textContent = '✅ Сақлаш';
#             }
#         }
        
#         // Doctor form submission
#         async function handleDoctorFormSubmit(e) {
#             e.preventDefault();
            
#             elements.doctorSubmitBtn.disabled = true;
#             elements.doctorSubmitBtn.textContent = '⏳ Қўшилмоқда...';
            
#             showLoading(true);
#             hideMessage();
            
#             const formData = new FormData(elements.doctorForm);
            
#             // Handle editable selects for doctor form
#             const mpHidden = document.querySelector('input[name="doctor_mp"]');
#             if (mpHidden && mpHidden.value) {
#                 formData.set('doctor_mp', mpHidden.value);
#             }
            
#             try {
#                 const response = await fetch('/add_doctor/', {
#                     method: 'POST',
#                     body: formData
#                 });
                
#                 const result = await response.json();
                
#                 if (result.success) {
#                     showMessage(result.message, 'success');
#                     elements.doctorForm.reset();
                    
#                     // Reset editable selects
#                     const mpHiddenInput = document.querySelector('input[name="doctor_mp"]');
#                     if (mpHiddenInput) mpHiddenInput.value = '';
#                 } else {
#                     showMessage(result.message, 'error');
#                 }
#             } catch (error) {
#                 showMessage('Хатолик юз берди: ' + error.message, 'error');
#             } finally {
#                 showLoading(false);
#                 elements.doctorSubmitBtn.disabled = false;
#                 elements.doctorSubmitBtn.textContent = '➕ Врач қўшиш';
#             }
#         }
        
#         function showMessage(text, type) {
#             elements.message.textContent = text;
#             elements.message.className = `message ${type}`;
#             elements.message.style.display = 'block';
            
#             if (type === 'success') {
#                 setTimeout(() => {
#                     hideMessage();
#                 }, 5000);
#             }
#         }
        
#         function hideMessage() {
#             elements.message.style.display = 'none';
#         }
        
#         function showLoading(show) {
#             elements.loading.style.display = show ? 'block' : 'none';
#         }
        
#         // Touch events for better mobile experience
#         if ('ontouchstart' in window) {
#             document.addEventListener('touchstart', function() {}, {passive: true});
#         }
#         </script>
#     </body>
#     </html>
#     """
#     return HTMLResponse(content=html_content)

# @app.get("/get_names/")
# async def get_names(username: str = Depends(authenticate)):
#     """Fast cached names endpoint"""
#     data = get_cached_sheets_data()
#     return {"names": data['ismlar'] if data else []}

# @app.get("/get_regions/")
# async def get_regions(username: str = Depends(authenticate)):
#     """Fast cached regions endpoint"""
#     data = get_cached_sheets_data()
#     return {"regions": data['regionlar'] if data else []}

# @app.post("/recommend_doctor/")
# async def recommend_doctor(doctor_name: str = Form(...), username: str = Depends(authenticate)):
#     """Async doctor recommendations"""
#     data = get_cached_sheets_data()
#     if not data:
#         return {"recommendations": []}
    
#     recommendations = await asyncio.to_thread(
#         get_recommendations_fast, doctor_name, data['shifokorlar']
#     )
#     return {"recommendations": recommendations}

# @app.post("/recommend_pharmacy/")
# async def recommend_pharmacy(pharmacy_name: str = Form(...), username: str = Depends(authenticate)):
#     """Async pharmacy recommendations"""
#     data = get_cached_sheets_data()
#     if not data:
#         return {"recommendations": []}
    
#     recommendations = await asyncio.to_thread(
#         get_recommendations_fast, pharmacy_name, data['dorixonalar']
#     )
#     return {"recommendations": recommendations}

# @app.post("/add_doctor/")
# async def add_doctor(
#     doctor_region: str = Form(...),
#     doctor_mp: str = Form(...),
#     dori_nomi: str = Form(...),
#     lpu: str = Form(...),
#     mutaxasislik: str = Form(...),
#     tel_no: str = Form(...),
#     doctor_name: str = Form(...),
#     username: str = Depends(authenticate)
# ):
#     """Add new doctor to YangiVrach sheet with new order"""
#     if not client:
#         return {"success": False, "message": "Google Sheets bilan bog'lanish xatosi"}
    
#     # Validate all required fields
#     if not all([doctor_region.strip(), doctor_mp.strip(), dori_nomi.strip(), 
#                 lpu.strip(), mutaxasislik.strip(), tel_no.strip(), doctor_name.strip()]):
#         return {"success": False, "message": "Барча майдонларни тўлдириш керак!"}
    
#     # Validate phone number format
#     if not tel_no.startswith('+998') and not tel_no.startswith('998'):
#         if tel_no.startswith('9') and len(tel_no) == 9:
#             tel_no = '+998' + tel_no
#         else:
#             return {"success": False, "message": "Телефон рақами нотўғри форматда! (+998901234567)"}
    
#     try:
#         # Prepare data with timestamp in the new order: Region, MP, Dori nomi, LPU, Mutaxasislik, Tel-no, Vrach ism-familiya, Data
#         vaqt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         yangi_qator = [
#             doctor_region.strip(),  # Region
#             doctor_mp.strip(),      # MP
#             dori_nomi.strip(),      # Dori nomi
#             lpu.strip(),            # LPU
#             mutaxasislik.strip(),   # Mutaxasislik
#             tel_no.strip(),         # Tel-no
#             doctor_name.strip(),    # Vrach ism-familiya
#             vaqt                    # Data
#         ]
        
#         # Save to YangiVrach sheet
#         spreadsheet = client.open("DoriXarajatlar")
#         yangi_vrach_sheet = spreadsheet.worksheet("YangiVrach")
#         await asyncio.to_thread(yangi_vrach_sheet.append_row, yangi_qator)
        
#         # Clear cache to reload data (optional - for immediate updates)
#         global _cached_data
#         _cached_data = None
#         # get_cached_sheets_data.cache_clear()
        
#         return {"success": True, "message": "✅ Янги врач муваффақиятли қўшилди!"}
        
#     except Exception as e:
#         return {"success": False, "message": f"Хатолик: {str(e)}"}

# @app.post("/save_data/")
# async def save_data(
#     ism: str = Form(...),
#     region: str = Form(...),
#     vrach: str = Form(...),
#     harajat_turi: str = Form(...),
#     apteka: str = Form(...),
#     summa_bonus: float = Form(...),
#     kompaniya_turi: str = Form(...),
#     izoh: str = Form(...),
#     username: str = Depends(authenticate)
# ):
#     """Optimized save function"""
#     data = get_cached_sheets_data()
#     if not data or not client:
#         return {"success": False, "message": "Google Sheets bilan bog'lanish xatoli"}
    
#     def find_exact_match(user_input, options):
#         user_input_norm = unidecode(user_input).lower().strip()
#         for opt in options:
#             if user_input_norm == unidecode(opt).lower().strip():
#                 return opt
#         return None
    
#     # Validate all required fields
#     if not all([ism.strip(), region.strip(), vrach.strip(), apteka.strip(), 
#                 harajat_turi.strip(), kompaniya_turi.strip(), izoh.strip()]):
#         return {"success": False, "message": "Барча мажбурий майдонларни тўлдириш керак!"}
    
#     if summa_bonus <= 0:
#         return {"success": False, "message": "Сумма бонус 0 дан катта бўлиш керак!"}
    
#     # Check exact matches - allow custom entries for names and regions from editable selects
#     vrach_match = find_exact_match(vrach, data['shifokorlar'])
#     apteka_match = find_exact_match(apteka, data['dorixonalar'])
    
#     # For ism and region, accept either exact match or custom entry
#     ism_match = find_exact_match(ism, data['ismlar']) or ism.strip()
#     region_match = find_exact_match(region, data['regionlar']) or region.strip()
    
#     if not all([vrach_match, apteka_match]):
#         missing = []
#         if not vrach_match: missing.append("Врач")
#         if not apteka_match: missing.append("Аптека")
#         return {"success": False, "message": f"Қуйидагилар рўйхатда топилмади: {', '.join(missing)}. Тавсия этилган рўйхатдан танланг!"}
    
#     # Calculate month
#     if harajat_turi == "Аптека 100%":
#         oy = datetime.now().month
#     else:
#         hozirgi_oy = datetime.now().month
#         oy = hozirgi_oy + 1 if hozirgi_oy < 12 else 1
    
#     oy_nomi = calendar.month_name[oy]
#     oy_nomi_uz = {
#         "January": "Январ", "February": "Феврал", "March": "Март",
#         "April": "Апрел", "May": "Май", "June": "Июн",
#         "July": "Июл", "August": "Август", "September": "Сентябр",
#         "October": "Октябр", "November": "Ноябр", "December": "Декабр"
#     }[oy_nomi]
    
#     vaqt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     yangi_qator = [
#         ism_match, region_match, vaqt, vrach_match, harajat_turi,
#         apteka_match, summa_bonus, oy_nomi_uz, kompaniya_turi, izoh.strip()
#     ]
    
#     try:
#         spreadsheet = client.open("DoriXarajatlar")
#         kiritmalar_sheet = spreadsheet.worksheet("Kiritmalar")
#         await asyncio.to_thread(kiritmalar_sheet.append_row, yangi_qator)
        
#         return {"success": True, "message": "✅ Маълумот муваффақиятли сақланди!"}
#     except Exception as e:
#         return {"success": False, "message": f"Хатолик: {str(e)}"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8080)





























































# from fastapi import FastAPI, Form, Request, HTTPException, Depends
# from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
# from fastapi.security import HTTPBasic, HTTPBasicCredentials
# import gspread
# from google.oauth2.service_account import Credentials
# from datetime import datetime
# import calendar
# from unidecode import unidecode
# import secrets
# import os
# import json
# import asyncio
# from functools import lru_cache
# from typing import List, Optional

# app = FastAPI()
# security = HTTPBasic()

# # Auth credentials
# VALID_USERNAME = "MarketingPFL"
# VALID_PASSWORD = "yordamkerak"

# def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
#     is_correct_username = secrets.compare_digest(credentials.username, VALID_USERNAME)
#     is_correct_password = secrets.compare_digest(credentials.password, VALID_PASSWORD)
#     if not (is_correct_username and is_correct_password):
#         raise HTTPException(
#             status_code=401,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Basic"},
#         )
#     return credentials.username

# def get_google_credentials():
#     try:
#         creds_path = "credentials.json"
#         SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#         creds = Credentials.from_service_account_file(creds_path, scopes=SCOPE)
#         return gspread.authorize(creds)
#     except Exception as e:
#         print(f"Error getting credentials: {e}")
#         return None

# # Global variables with caching
# client = None
# _cached_data = None

# @lru_cache(maxsize=1)
# def get_cached_sheets_data():
#     global client, _cached_data
#     try:
#         if not client:
#             client = get_google_credentials()
        
#         if client and not _cached_data:
#             SPREADSHEET_NAME = "DoriXarajatlar"
#             spreadsheet = client.open(SPREADSHEET_NAME)
            
#             shifokorlar_sheet = spreadsheet.worksheet("Shifokorlar")
#             dorixonalar_sheet = spreadsheet.worksheet("Dorixonalar")
#             ismlar_sheet = spreadsheet.worksheet("IsmFamiliya")
#             regionlar_sheet = spreadsheet.worksheet("Regionlar")
            
#             shifokorlar = shifokorlar_sheet.col_values(1)[1:]
#             dorixonalar = dorixonalar_sheet.col_values(1)[1:]
#             ismlar = ismlar_sheet.col_values(1)[1:]
#             regionlar = regionlar_sheet.col_values(1)[1:]
            
#             _cached_data = {
#                 'shifokorlar': shifokorlar,
#                 'dorixonalar': dorixonalar,
#                 'ismlar': ismlar,
#                 'regionlar': regionlar
#             }
            
#         return _cached_data
#     except Exception as e:
#         print(f"Error getting cached data: {e}")
#         return None

# def get_recommendations_fast(user_input: str, options: List[str], limit: int = 10) -> List[str]:
#     if not user_input or len(user_input) < 1:
#         return []
    
#     user_input_norm = unidecode(user_input).lower()
#     matches = []
    
#     for opt in options:
#         opt_norm = unidecode(opt).lower()
#         if user_input_norm == opt_norm:
#             return [opt]
#         elif user_input_norm in opt_norm:
#             score = len(user_input_norm) / len(opt_norm)
#             matches.append((opt, score))
            
#             if len(matches) >= limit * 2:
#                 break
    
#     matches.sort(key=lambda x: x[1], reverse=True)
#     return [match[0] for match in matches[:limit]]

# # Yangi: Keshni davriy yangilash funksiyasi
# async def refresh_cache_periodically():
#     while True:
#         print("Refreshing cached data...")
#         get_cached_sheets_data.cache_clear() # Keshni tozalash
#         data = get_cached_sheets_data() # Ma'lumotlarni qayta yuklash
#         if data:
#             print("✅ Cached data refreshed successfully")
#         else:
#             print("⚠️ Warning: Could not refresh Google Sheets data")
#         await asyncio.sleep(300) # Har 5 daqiqada (300 soniya) yangilash

# @app.on_event("startup")
# async def startup_event():
#     print("Initializing data...")
#     data = get_cached_sheets_data()
#     if data:
#         print("✅ Data loaded successfully")
#     else:
#         print("⚠️ Warning: Could not initialize Google Sheets")
    
#     # Keshni davriy yangilash vazifasini ishga tushirish
#     asyncio.create_task(refresh_cache_periodically())

# @app.get("/", response_class=HTMLResponse)
# async def main_page(request: Request, username: str = Depends(authenticate)):
#     html_content = """
#     <!DOCTYPE html>
#     <html lang="uz">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>💊 Дори харажатлари</title>
#         <style>
#             * { margin: 0; padding: 0; box-sizing: border-box; }
            
#             body {
#                 font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
#                 background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#                 min-height: 100vh;
#                 padding: 10px;
#             }
            
#             .container {
#                 max-width: 1000px;
#                 margin: 0 auto;
#                 background: white;
#                 border-radius: 15px;
#                 box-shadow: 0 20px 40px rgba(0,0,0,0.1);
#                 overflow: hidden;
#                 position: relative;
#             }
            
#             .header {
#                 background: linear-gradient(45deg, #667eea, #764ba2);
#                 color: white;
#                 padding: 20px;
#                 text-align: center;
#                 position: relative;
#             }
            
#             .sidebar-toggle {
#                 position: absolute;
#                 top: 50%;
#                 left: 20px;
#                 transform: translateY(-50%);
#                 background: rgba(255,255,255,0.2);
#                 border: none;
#                 color: white;
#                 padding: 10px;
#                 border-radius: 8px;
#                 cursor: pointer;
#                 font-size: 18px;
#                 transition: background 0.2s;
#             }
            
#             .sidebar-toggle:hover {
#                 background: rgba(255,255,255,0.3);
#             }
            
#             .sidebar {
#                 position: fixed;
#                 top: 0;
#                 left: -300px;
#                 width: 300px;
#                 height: 100vh;
#                 background: white;
#                 box-shadow: 2px 0 10px rgba(0,0,0,0.1);
#                 transition: left 0.3s ease;
#                 z-index: 2000;
#                 padding: 20px;
#             }
            
#             .sidebar.active {
#                 left: 0;
#             }
            
#             .sidebar-header {
#                 padding-bottom: 20px;
#                 border-bottom: 1px solid #eee;
#                 margin-bottom: 20px;
#             }
            
#             .sidebar-close {
#                 float: right;
#                 background: none;
#                 border: none;
#                 font-size: 24px;
#                 cursor: pointer;
#                 color: #666;
#             }
            
#             .sidebar-menu {
#                 list-style: none;
#             }
            
#             .sidebar-menu li {
#                 margin-bottom: 10px;
#             }
            
#             .sidebar-menu a {
#                 display: block;
#                 padding: 15px;
#                 text-decoration: none;
#                 color: #333;
#                 border-radius: 8px;
#                 transition: all 0.2s;
#             }
            
#             .sidebar-menu a:hover, .sidebar-menu a.active {
#                 background: #f8f9fa;
#                 color: #667eea;
#             }
            
#             .overlay {
#                 position: fixed;
#                 top: 0;
#                 left: 0;
#                 width: 100vw;
#                 height: 100vh;
#                 background: rgba(0,0,0,0.5);
#                 z-index: 1500;
#                 display: none;
#             }
            
#             .overlay.active {
#                 display: block;
#             }
            
#             .content {
#                 padding: 30px;
#             }
            
#             .section {
#                 display: none;
#             }
            
#             .section.active {
#                 display: block;
#             }
            
#             .form-row {
#                 display: flex;
#                 gap: 15px;
#                 margin-bottom: 20px;
#                 flex-wrap: wrap;
#             }
            
#             .form-group {
#                 position: relative;
#                 flex: 1;
#                 min-width: 250px;
#             }
            
#             .form-group.full-width {
#                 flex: 100%;
#                 min-width: 100%;
#             }
            
#             label {
#                 display: block;
#                 margin-bottom: 8px;
#                 font-weight: 600;
#                 color: #333;
#                 font-size: 14px;
#             }
            
#             .required { color: #e74c3c; }
            
#             input, select, textarea {
#                 width: 100%;
#                 padding: 12px;
#                 border: 2px solid #e1e5e9;
#                 border-radius: 8px;
#                 font-size: 16px;
#                 transition: border-color 0.2s;
#                 background-color: #fff;
#             }
            
#             /* Editable select styles */
#             select[data-editable="true"] {
#                 background: white url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="12" height="8" viewBox="0 0 12 8"><path fill="%23666" d="M6 8L0 2h12z"/></svg>') no-repeat right 12px center;
#                 appearance: none;
#                 -webkit-appearance: none;
#                 -moz-appearance: none;
#             }
            
#             input:focus, select:focus, textarea:focus {
#                 outline: none;
#                 border-color: #667eea;
#                 box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
#             }
            
#             .suggestions {
#                 position: absolute;
#                 top: 100%;
#                 left: 0;
#                 right: 0;
#                 background: white;
#                 border: 1px solid #e1e5e9;
#                 border-top: none;
#                 border-radius: 0 0 8px 8px;
#                 max-height: 200px;
#                 overflow-y: auto;
#                 z-index: 1000;
#                 box-shadow: 0 4px 15px rgba(0,0,0,0.15);
#                 display: none;
#             }
            
#             .suggestion-item {
#                 padding: 12px;
#                 cursor: pointer;
#                 border-bottom: 1px solid #f1f1f1;
#                 transition: background-color 0.15s;
#             }
            
#             .suggestion-item:hover, .suggestion-item.active {
#                 background-color: #f8f9fa;
#             }
            
#             .suggestion-item:last-child { border-bottom: none; }
            
#             .btn {
#                 background: linear-gradient(45deg, #667eea, #764ba2);
#                 color: white;
#                 padding: 15px 30px;
#                 border: none;
#                 border-radius: 8px;
#                 font-size: 16px;
#                 cursor: pointer;
#                 transition: all 0.2s;
#                 font-weight: 600;
#                 min-width: 150px;
#             }
            
#             .btn:hover {
#                 transform: translateY(-2px);
#                 box-shadow: 0 5px 15px rgba(102,126,234,0.4);
#             }
            
#             .btn:active { transform: translateY(0); }
            
#             .btn:disabled {
#                 opacity: 0.6;
#                 cursor: not-allowed;
#                 transform: none;
#             }
            
#             .btn-secondary {
#                 background: linear-gradient(45deg, #28a745, #20c997);
#             }
            
#             .btn-secondary:hover {
#                 box-shadow: 0 5px 15px rgba(40,167,69,0.4);
#             }
            
#             .message {
#                 padding: 15px;
#                 margin: 15px 0;
#                 border-radius: 8px;
#                 font-weight: 500;
#                 display: none;
#             }
            
#             .success {
#                 background: #d4edda;
#                 color: #155724;
#                 border-left: 4px solid #28a745;
#             }
            
#             .error {
#                 background: #f8d7da;
#                 color: #721c24;
#                 border-left: 4px solid #dc3545;
#             }
            
#             .loading {
#                 display: none;
#                 text-align: center;
#                 padding: 20px;
#             }
            
#             .spinner {
#                 border: 3px solid #f3f3f3;
#                 border-top: 3px solid #667eea;
#                 border-radius: 50%;
#                 width: 30px;
#                 height: 30px;
#                 animation: spin 1s linear infinite;
#                 margin: 0 auto 10px;
#             }
            
#             @keyframes spin {
#                 0% { transform: rotate(0deg); }
#                 100% { transform: rotate(360deg); }
#             }
            
#             .legend {
#                 background: #f8f9fa;
#                 padding: 15px;
#                 border-radius: 8px;
#                 margin-top: 20px;
#                 text-align: center;
#                 color: #666;
#                 font-size: 14px;
#             }
            
#             .search-indicator {
#                 position: absolute;
#                 right: 12px;
#                 top: 50%;
#                 transform: translateY(-50%);
#                 color: #666;
#                 font-size: 12px;
#                 display: none;
#             }
            
#             /* Mobile Responsive */
#             @media (max-width: 768px) {
#                 body {
#                     padding: 5px;
#                 }
                
#                 .container {
#                     border-radius: 10px;
#                 }
                
#                 .header {
#                     padding: 15px;
#                 }
                
#                 .header h1 {
#                     font-size: 20px;
#                     margin-top: 10px;
#                 }
                
#                 .content {
#                     padding: 15px;
#                 }
                
#                 .form-row {
#                     flex-direction: column;
#                     gap: 10px;
#                 }
                
#                 .form-group {
#                     min-width: 100%;
#                 }
                
#                 input, select, textarea {
#                     font-size: 16px; /* Prevents zoom on iOS */
#                     padding: 15px 12px;
#                 }
                
#                 .btn {
#                     width: 100%;
#                     padding: 18px;
#                     font-size: 18px;
#                 }
                
#                 .sidebar {
#                     width: 280px;
#                 }
                
#                 .sidebar-toggle {
#                     left: 15px;
#                     padding: 8px;
#                 }
#             }
            
#             @media (max-width: 480px) {
#                 .header h1 {
#                     font-size: 18px;
#                 }
                
#                 .content {
#                     padding: 10px;
#                 }
                
#                 .sidebar {
#                     width: 100%;
#                     left: -100%;
#                 }
#             }
#         </style>
#     </head>
#     <body>
#         <!-- Sidebar -->
#         <div id="sidebar" class="sidebar">
#             <div class="sidebar-header">
#                 <h3>📋 Меню</h3>
#                 <button class="sidebar-close" onclick="toggleSidebar()">×</button>
#             </div>
#             <ul class="sidebar-menu">
#                 <li><a href="#" class="menu-item active" data-section="main-form">📊 Асосий форма</a></li>
#                 <li><a href="#" class="menu-item" data-section="add-doctor">👨‍⚕️ Янги врач қўшиш</a></li>
#             </ul>
#         </div>
        
#         <div id="overlay" class="overlay" onclick="toggleSidebar()"></div>
        
#         <div class="container">
#             <div class="header">
#                 <button class="sidebar-toggle" onclick="toggleSidebar()">☰</button>
#                 <h1>💊 Маркетинг учун рўйхат</h1>
#             </div>
            
#             <div class="content">
#                 <!-- Main Form Section -->
#                 <div id="main-form" class="section active">
#                     <form id="mainForm">
#                         <div class="form-row">
#                             <div class="form-group">
#                                 <label for="ism">👤 Исм-Фамилия <span class="required">*</span></label>
#                                 <select id="ism" name="ism" required data-editable="true">
#                                     <option value="">Танланг ёки киритинг...</option>
#                                 </select>
#                             </div>
#                             <div class="form-group">
#                                 <label for="region">📍 Регион <span class="required">*</span></label>
#                                 <select id="region" name="region" required>
#                                     <option value="">Танланг...</option>
#                                 </select>
#                             </div>
#                         </div>

#                         <div class="form-row">
#                             <div class="form-group">
#                                 <label for="vrach">👨‍⚕️ Врач <span class="required">*</span></label>
#                                 <input type="text" id="vrach" name="vrach" required autocomplete="off" 
#                                        placeholder="Врач номини киритинг...">
#                                 <div class="search-indicator" id="vrach-indicator">🔍</div>
#                                 <div id="vrach-suggestions" class="suggestions"></div>
#                             </div>
#                             <div class="form-group">
#                                 <label for="harajat_turi">💼 Инвеститция тури <span class="required">*</span></label>
#                                 <select id="harajat_turi" name="harajat_turi" required>
#                                     <option value="">Танланг...</option>
#                                     <option value="Аптека 100%">Аптека 100%</option>
#                                     <option value="Оптовик маркетинг 23%">Оптовик маркетинг 23%</option>
#                                     <option value="Предоплата маркетинг">Предоплата маркетинг</option>
#                                     <option value="Аванс маркетинг">Аванс маркетинг</option>
#                                 </select>
#                             </div>
#                         </div>

#                         <div class="form-row">
#                             <div class="form-group">
#                                 <label for="apteka">🏥 Аптека <span class="required">*</span></label>
#                                 <input type="text" id="apteka" name="apteka" required autocomplete="off"
#                                        placeholder="Аптека номини киритинг...">
#                                 <div class="search-indicator" id="apteka-indicator">🔍</div>
#                                 <div id="apteka-suggestions" class="suggestions"></div>
#                             </div>
#                             <div class="form-group">
#                                 <label for="summa_bonus">💰 Сумма бонус <span class="required">*</span></label>
#                                 <input type="number" id="summa_bonus" name="summa_bonus" step="0.01" 
#                                        min="0.01" required placeholder="0.00">
#                             </div>
#                         </div>

#                         <div class="form-row">
#                             <div class="form-group">
#                                 <label for="kompaniya_turi">🏢 Бренд <span class="required">*</span></label>
#                                 <select id="kompaniya_turi" name="kompaniya_turi" required>
#                                     <option value="">Танланг...</option>
#                                     <option value="GMX">GMX</option>
#                                     <option value="BP">BP</option>
#                                 </select>
#                             </div>
#                             <div class="form-group">
#                                 <label for="izoh">📝 Изоҳ <span class="required">*</span></label>
#                                 <textarea id="izoh" name="izoh" rows="3" required 
#                                           placeholder="Изоҳ киритинг..."></textarea>
#                             </div>
#                         </div>

#                         <div style="text-align: center; margin-top: 30px;">
#                             <button type="submit" class="btn" id="submitBtn">
#                                 ✅ Сақлаш
#                             </button>
#                         </div>
#                     </form>
#                 </div>
                
#                 <!-- Add Doctor Section -->
#                 <div id="add-doctor" class="section">
#                     <h2>👨‍⚕️ Янги врач қўшиш</h2>
#                     <form id="doctorForm">
#                         <div class="form-row">
#                             <div class="form-group">
#                                 <label for="doctor_region">📍 Регион <span class="required">*</span></label>
#                                 <select id="doctor_region" name="doctor_region" required>
#                                     <option value="">Танланг...</option>
#                                 </select>
#                             </div>
#                             <div class="form-group">
#                                 <label for="doctor_mp">👤 МП <span class="required">*</span></label>
#                                 <select id="doctor_mp" name="doctor_mp" required data-editable="true">
#                                     <option value="">Танланг ёки киритинг...</option>
#                                 </select>
#                             </div>
#                         </div>
                        
#                         <div class="form-row">
#                             <div class="form-group">
#                                 <label for="dori_nomi">💊 Дори номи <span class="required">*</span></label>
#                                 <input type="text" id="dori_nomi" name="dori_nomi" required 
#                                        placeholder="Дори номини киритинг...">
#                             </div>
#                             <div class="form-group">
#                                 <label for="lpu">🏥 ЛПУ <span class="required">*</span></label>
#                                 <input type="text" id="lpu" name="lpu" required 
#                                        placeholder="ЛПУ номини киритинг...">
#                             </div>
#                         </div>
                        
#                         <div class="form-row">
#                             <div class="form-group">
#                                 <label for="mutaxasislik">🩺 Мутахассислик <span class="required">*</span></label>
#                                 <input type="text" id="mutaxasislik" name="mutaxasislik" required 
#                                        placeholder="Мутахассислик киритинг...">
#                             </div>
#                             <div class="form-group">
#                                 <label for="tel_no">📞 Телефон рақами <span class="required">*</span></label>
#                                 <input type="tel" id="tel_no" name="tel_no" required 
#                                        placeholder="+998901234567">
#                             </div>
#                         </div>
                        
#                         <div class="form-row">
#                             <div class="form-group full-width">
#                                 <label for="doctor_name">👨‍⚕️ Врач исм-фамилияси <span class="required">*</span></label>
#                                 <input type="text" id="doctor_name" name="doctor_name" required 
#                                        placeholder="Исм-фамилия киритинг...">
#                             </div>
#                         </div>
                        
#                         <div style="text-align: center; margin-top: 30px;">
#                             <button type="submit" class="btn btn-secondary" id="doctorSubmitBtn">
#                                 ➕ Врач қўшиш
#                             </button>
#                         </div>
#                     </form>
#                 </div>
                
#                 <div id="loading" class="loading">
#                     <div class="spinner"></div>
#                     <p>Юкланмоқда...</p>
#                 </div>
                
#                 <div id="message" class="message"></div>
                
#                 <div class="legend">
#                     <span class="required">*</span> - Мажбурий майдонлар
#                 </div>
#             </div>
#         </div>
        
#         <script>
#         // Global variables
#         let debounceTimers = {};
#         let cachedData = { doctors: [], pharmacies: [], names: [], regions: [] };
        
#         const elements = {
#             ism: null, region: null, vrach: null, apteka: null,
#             doctorRegion: null, doctorMp: null,
#             vrachSuggestions: null, aptekaSuggestions: null,
#             vrachIndicator: null, aptekaIndicator: null,
#             form: null, doctorForm: null, message: null, loading: null,
#             submitBtn: null, doctorSubmitBtn: null
#         };
        
#         // Initialize
#         document.addEventListener('DOMContentLoaded', function() {
#             cacheElements();
#             initializeData();
#             setupEventListeners();
#             setupEditableSelects();
#         });
        
#         function cacheElements() {
#             elements.ism = document.getElementById('ism');
#             elements.region = document.getElementById('region');
#             elements.vrach = document.getElementById('vrach');
#             elements.apteka = document.getElementById('apteka');
#             elements.doctorRegion = document.getElementById('doctor_region');
#             elements.doctorMp = document.getElementById('doctor_mp');
#             elements.vrachSuggestions = document.getElementById('vrach-suggestions');
#             elements.aptekaSuggestions = document.getElementById('apteka-suggestions');
#             elements.vrachIndicator = document.getElementById('vrach-indicator');
#             elements.aptekaIndicator = document.getElementById('apteka-indicator');
#             elements.form = document.getElementById('mainForm');
#             elements.doctorForm = document.getElementById('doctorForm');
#             elements.message = document.getElementById('message');
#             elements.loading = document.getElementById('loading');
#             elements.submitBtn = document.getElementById('submitBtn');
#             elements.doctorSubmitBtn = document.getElementById('doctorSubmitBtn');
#         }
        
#         async function initializeData() {
#             try {
#                 await Promise.all([loadNames(), loadRegions()]);
#                 console.log('✅ Data loaded successfully');
#             } catch (error) {
#                 console.error('❌ Error loading data:', error);
#                 showMessage('Маълумотлар юклашда хатолик юз берди', 'error');
#             }
#         }
        
#         async function loadNames() {
#             const response = await fetch('/get_names/');
#             const data = await response.json();
#             cachedData.names = data.names;
            
#             // Clear existing options before adding new ones
#             elements.ism.innerHTML = '<option value="">Танланг ёки киритинг...</option>';
#             elements.doctorMp.innerHTML = '<option value="">Танланг ёки киритинг...</option>';

#             // Load names for main form
#             const fragment1 = document.createDocumentFragment();
#             data.names.forEach(name => {
#                 const option = document.createElement('option');
#                 option.value = name;
#                 option.textContent = name;
#                 fragment1.appendChild(option);
#             });
#             elements.ism.appendChild(fragment1);
            
#             // Load names for MP dropdown in doctor form
#             const fragment2 = document.createDocumentFragment();
#             data.names.forEach(name => {
#                 const option = document.createElement('option');
#                 option.value = name;
#                 option.textContent = name;
#                 fragment2.appendChild(option);
#             });
#             elements.doctorMp.appendChild(fragment2);
#         }
        
#         async function loadRegions() {
#             const response = await fetch('/get_regions/');
#             const data = await response.json();
#             cachedData.regions = data.regions;

#             // Clear existing options before adding new ones
#             elements.region.innerHTML = '<option value="">Танланг...</option>';
#             elements.doctorRegion.innerHTML = '<option value="">Танланг...</option>';
            
#             // Load regions for main form
#             const fragment1 = document.createDocumentFragment();
#             data.regions.forEach(region => {
#                 const option = document.createElement('option');
#                 option.value = region;
#                 option.textContent = region;
#                 fragment1.appendChild(option);
#             });
#             elements.region.appendChild(fragment1);
            
#             // Load regions for doctor form
#             const fragment2 = document.createDocumentFragment();
#             data.regions.forEach(region => {
#                 const option = document.createElement('option');
#                 option.value = region;
#                 option.textContent = region;
#                 fragment2.appendChild(option);
#             });
#             elements.doctorRegion.appendChild(fragment2);
#         }
        
#         function setupEditableSelects() {
#             // Make selects with data-editable="true" behave like editable dropdowns
#             document.querySelectorAll('select[data-editable="true"]').forEach(select => {
#                 // Create hidden input for custom values
#                 let hiddenInput = select.parentNode.querySelector(`input[name="${select.name}"]`);
#                 if (!hiddenInput) { // Create only if it doesn't exist
#                     hiddenInput = document.createElement('input');
#                     hiddenInput.type = 'hidden';
#                     hiddenInput.name = select.name;
#                     select.parentNode.insertBefore(hiddenInput, select.nextSibling);
#                 }
                
#                 // Handle select change
#                 select.addEventListener('change', function() {
#                     hiddenInput.value = this.value;
#                 });
                
#                 // Allow typing by converting to input-like behavior
#                 select.addEventListener('keydown', function(e) {
#                     if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey) { // Single character key, not a modifier
#                         // Convert to searchable mode
#                         this.setAttribute('data-search-mode', 'true');
#                         this.style.color = '#666';
                        
#                         // Create a temporary option for search
#                         let searchOption = this.querySelector('option[data-search]');
#                         if (!searchOption) {
#                             searchOption = document.createElement('option');
#                             searchOption.setAttribute('data-search', 'true');
#                             searchOption.value = '';
#                             this.insertBefore(searchOption, this.firstChild);
#                         }
                        
#                         searchOption.textContent = e.key;
#                         searchOption.selected = true;
#                         hiddenInput.value = e.key;
                        
#                         // Prevent default select behavior
#                         e.preventDefault();
#                     }
#                 });
                
#                 // Handle further typing
#                 select.addEventListener('keyup', function(e) {
#                     if (this.getAttribute('data-search-mode') === 'true') {
#                         const searchOption = this.querySelector('option[data-search]');
#                         if (searchOption) {
#                             if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey) {
#                                 searchOption.textContent += e.key;
#                                 hiddenInput.value = searchOption.textContent;
#                             } else if ((e.key === 'Backspace' || e.key === 'Delete')) {
#                                 let currentText = searchOption.textContent;
#                                 if (currentText.length > 0) {
#                                     searchOption.textContent = currentText.slice(0, -1);
#                                     hiddenInput.value = searchOption.textContent;
#                                 }
#                             }
#                         }
#                     }
#                 });
                
#                 // Reset search mode on blur
#                 select.addEventListener('blur', function() {
#                     this.removeAttribute('data-search-mode');
#                     this.style.color = '';
#                     const searchOption = this.querySelector('option[data-search]');
#                     if (searchOption && searchOption.textContent.trim() === '') {
#                         searchOption.remove();
#                     } else if (searchOption) {
#                         // If there's text in searchOption, make it the selected value
#                         select.value = searchOption.textContent;
#                         hiddenInput.value = searchOption.textContent;
#                         searchOption.remove(); // Remove the temporary search option
#                     }
#                 });

#                 // Ensure hidden input is updated on initial load if a value is pre-selected
#                 if (select.value) {
#                     hiddenInput.value = select.value;
#                 }
#             });
#         }
        
#         function setupEventListeners() {
#             // Search functionality
#             elements.vrach?.addEventListener('input', (e) => handleSearch(e, 'vrach'));
#             elements.apteka?.addEventListener('input', (e) => handleSearch(e, 'apteka'));
            
#             // Hide suggestions on outside click
#             document.addEventListener('click', (e) => {
#                 if (!e.target.closest('.form-group')) {
#                     hideSuggestions();
#                 }
#             });
            
#             // Form submissions
#             elements.form?.addEventListener('submit', handleMainFormSubmit);
#             elements.doctorForm?.addEventListener('submit', handleDoctorFormSubmit);
            
#             // Menu navigation
#             document.querySelectorAll('.menu-item').forEach(item => {
#                 item.addEventListener('click', (e) => {
#                     e.preventDefault();
#                     const section = e.target.dataset.section;
#                     showSection(section);
                    
#                     // Update active menu item
#                     document.querySelectorAll('.menu-item').forEach(mi => mi.classList.remove('active'));
#                     e.target.classList.add('active');
                    
#                     // Close sidebar on mobile
#                     if (window.innerWidth <= 768) {
#                         toggleSidebar();
#                     }
#                 });
#             });
#         }
        
#         function toggleSidebar() {
#             const sidebar = document.getElementById('sidebar');
#             const overlay = document.getElementById('overlay');
            
#             sidebar.classList.toggle('active');
#             overlay.classList.toggle('active');
#         }
        
#         function showSection(sectionId) {
#             document.querySelectorAll('.section').forEach(section => {
#                 section.classList.remove('active');
#             });
#             document.getElementById(sectionId).classList.add('active');
#         }
        
#         function handleSearch(e, type) {
#             const value = e.target.value;
#             const indicator = type === 'vrach' ? elements.vrachIndicator : elements.aptekaIndicator;
            
#             clearTimeout(debounceTimers[type]);
            
#             if (value.length >= 1) {
#                 indicator.style.display = 'block';
#                 debounceTimers[type] = setTimeout(() => {
#                     performSearch(value, type);
#                 }, 200);
#             } else {
#                 indicator.style.display = 'none';
#                 hideSuggestions(type);
#             }
#         }
        
#         async function performSearch(query, type) {
#             try {
#                 const endpoint = type === 'vrach' ? '/recommend_doctor/' : '/recommend_pharmacy/';
#                 const paramName = type === 'vrach' ? 'doctor_name' : 'pharmacy_name';
                
#                 const formData = new FormData();
#                 formData.append(paramName, query);
                
#                 const response = await fetch(endpoint, {
#                     method: 'POST',
#                     body: formData
#                 });
                
#                 const data = await response.json();
#                 displaySuggestions(type, data.recommendations);
                
#             } catch (error) {
#                 console.error(`Search error for ${type}:`, error);
#             } finally {
#                 const indicator = type === 'vrach' ? elements.vrachIndicator : elements.aptekaIndicator;
#                 indicator.style.display = 'none';
#             }
#         }
        
#         function displaySuggestions(type, suggestions) {
#             const container = type === 'vrach' ? elements.vrachSuggestions : elements.aptekaSuggestions;
#             const input = type === 'vrach' ? elements.vrach : elements.apteka;
            
#             container.innerHTML = '';
            
#             if (suggestions.length === 0) {
#                 container.style.display = 'none';
#                 return;
#             }
            
#             const fragment = document.createDocumentFragment();
#             suggestions.forEach(suggestion => {
#                 const div = document.createElement('div');
#                 div.className = 'suggestion-item';
#                 div.textContent = suggestion;
#                 div.addEventListener('click', () => {
#                     input.value = suggestion;
#                     hideSuggestions(type);
#                 });
#                 fragment.appendChild(div);
#             });
            
#             container.appendChild(fragment);
#             container.style.display = 'block';
#         }
        
#         function hideSuggestions(type) {
#             if (type) {
#                 const container = type === 'vrach' ? elements.vrachSuggestions : elements.aptekaSuggestions;
#                 container.style.display = 'none';
#             } else {
#                 elements.vrachSuggestions.style.display = 'none';
#                 elements.aptekaSuggestions.style.display = 'none';
#             }
#         }
        
#         // Main form submission
#         async function handleMainFormSubmit(e) {
#             e.preventDefault();
            
#             elements.submitBtn.disabled = true;
#             elements.submitBtn.textContent = '⏳ Сақланмоқда...';
            
#             showLoading(true);
#             hideMessage();
            
#             const formData = new FormData(elements.form);
            
#             // Handle editable selects
#             const ismHidden = document.querySelector('input[name="ism"]');
#             const regionHidden = document.querySelector('input[name="region"]');
            
#             if (ismHidden && ismHidden.value) {
#                 formData.set('ism', ismHidden.value);
#             }
#             // For region, it's a standard select, so its value is already in formData
#             // No need for regionHidden check unless it's also data-editable="true"
#             // If region is also editable, uncomment the following:
#             // if (regionHidden && regionHidden.value) {
#             //     formData.set('region', regionHidden.value);
#             // }
            
#             try {
#                 const response = await fetch('/save_data/', {
#                     method: 'POST',
#                     body: formData
#                 });
                
#                 const result = await response.json();
                
#                 if (result.success) {
#                     showMessage(result.message, 'success');
#                     elements.form.reset();
#                     elements.vrach.value = '';
#                     elements.apteka.value = '';
#                     hideSuggestions();
                    
#                     // Reset editable selects' hidden inputs
#                     document.querySelectorAll('select[data-editable="true"]').forEach(select => {
#                         const hiddenInput = select.parentNode.querySelector(`input[name="${select.name}"]`);
#                         if (hiddenInput) hiddenInput.value = '';
#                         select.value = ''; // Reset the select itself
#                     });

#                     // Re-load names and regions to reflect potential new custom entries
#                     await initializeData();

#                 } else {
#                     showMessage(result.message, 'error');
#                 }
#             } catch (error) {
#                 showMessage('Хатолик юз берди: ' + error.message, 'error');
#             } finally {
#                 showLoading(false);
#                 elements.submitBtn.disabled = false;
#                 elements.submitBtn.textContent = '✅ Сақлаш';
#             }
#         }
        
#         // Doctor form submission
#         async function handleDoctorFormSubmit(e) {
#             e.preventDefault();
            
#             elements.doctorSubmitBtn.disabled = true;
#             elements.doctorSubmitBtn.textContent = '⏳ Қўшилмоқда...';
            
#             showLoading(true);
#             hideMessage();
            
#             const formData = new FormData(elements.doctorForm);
            
#             // Handle editable selects for doctor form
#             const mpHidden = document.querySelector('input[name="doctor_mp"]');
#             if (mpHidden && mpHidden.value) {
#                 formData.set('doctor_mp', mpHidden.value);
#             }
            
#             try {
#                 const response = await fetch('/add_doctor/', {
#                     method: 'POST',
#                     body: formData
#                 });
                
#                 const result = await response.json();
                
#                 if (result.success) {
#                     showMessage(result.message, 'success');
#                     elements.doctorForm.reset();
                    
#                     // Reset editable selects' hidden inputs
#                     document.querySelectorAll('select[data-editable="true"]').forEach(select => {
#                         const hiddenInput = select.parentNode.querySelector(`input[name="${select.name}"]`);
#                         if (hiddenInput) hiddenInput.value = '';
#                         select.value = ''; // Reset the select itself
#                     });

#                     // Re-load names and regions to reflect potential new custom entries
#                     await initializeData();

#                 } else {
#                     showMessage(result.message, 'error');
#                 }
#             } catch (error) {
#                 showMessage('Хатолик юз берди: ' + error.message, 'error');
#             } finally {
#                 showLoading(false);
#                 elements.doctorSubmitBtn.disabled = false;
#                 elements.doctorSubmitBtn.textContent = '➕ Врач қўшиш';
#             }
#         }
        
#         function showMessage(text, type) {
#             elements.message.textContent = text;
#             elements.message.className = `message ${type}`;
#             elements.message.style.display = 'block';
            
#             if (type === 'success') {
#                 setTimeout(() => {
#                     hideMessage();
#                 }, 5000);
#             }
#         }
        
#         function hideMessage() {
#             elements.message.style.display = 'none';
#         }
        
#         function showLoading(show) {
#             elements.loading.style.display = show ? 'block' : 'none';
#         }
        
#         // Touch events for better mobile experience
#         if ('ontouchstart' in window) {
#             document.addEventListener('touchstart', function() {}, {passive: true});
#         }
#         </script>
#     </body>
#     </html>
#     """
#     return HTMLResponse(content=html_content)

# @app.get("/get_names/")
# async def get_names(username: str = Depends(authenticate)):
#     """Fast cached names endpoint"""
#     data = get_cached_sheets_data()
#     return {"names": data['ismlar'] if data else []}

# @app.get("/get_regions/")
# async def get_regions(username: str = Depends(authenticate)):
#     """Fast cached regions endpoint"""
#     data = get_cached_sheets_data()
#     return {"regions": data['regionlar'] if data else []}

# @app.post("/recommend_doctor/")
# async def recommend_doctor(doctor_name: str = Form(...), username: str = Depends(authenticate)):
#     """Async doctor recommendations"""
#     data = get_cached_sheets_data()
#     if not data:
#         return {"recommendations": []}
    
#     recommendations = await asyncio.to_thread(
#         get_recommendations_fast, doctor_name, data['shifokorlar']
#     )
#     return {"recommendations": recommendations}

# @app.post("/recommend_pharmacy/")
# async def recommend_pharmacy(pharmacy_name: str = Form(...), username: str = Depends(authenticate)):
#     """Async pharmacy recommendations"""
#     data = get_cached_sheets_data()
#     if not data:
#         return {"recommendations": []}
    
#     recommendations = await asyncio.to_thread(
#         get_recommendations_fast, pharmacy_name, data['dorixonalar']
#     )
#     return {"recommendations": recommendations}

# @app.post("/add_doctor/")
# async def add_doctor(
#     doctor_region: str = Form(...),
#     doctor_mp: str = Form(...),
#     dori_nomi: str = Form(...),
#     lpu: str = Form(...),
#     mutaxasislik: str = Form(...),
#     tel_no: str = Form(...),
#     doctor_name: str = Form(...),
#     username: str = Depends(authenticate)
# ):
#     """Add new doctor to YangiVrach sheet with new order"""
#     if not client:
#         return {"success": False, "message": "Google Sheets bilan bog'lanish xatosi"}
    
#     # Validate all required fields
#     if not all([doctor_region.strip(), doctor_mp.strip(), dori_nomi.strip(), 
#                 lpu.strip(), mutaxasislik.strip(), tel_no.strip(), doctor_name.strip()]):
#         return {"success": False, "message": "Барча майдонларни тўлдириш керак!"}
    
#     # Validate phone number format
#     # Allow 9-digit numbers starting with 9, and prepend +998
#     if not tel_no.startswith('+998'):
#         if tel_no.startswith('9') and len(tel_no) == 9:
#             tel_no = '+998' + tel_no
#         else:
#             return {"success": False, "message": "Телефон рақами нотўғри форматда! (+998901234567)"}
    
#     try:
#         # Prepare data with timestamp in the new order: Region, MP, Dori nomi, LPU, Mutaxasislik, Tel-no, Vrach ism-familiya, Data
#         vaqt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         yangi_qator = [
#             doctor_region.strip(),  # Region
#             doctor_mp.strip(),      # MP
#             dori_nomi.strip(),      # Dori nomi
#             lpu.strip(),            # LPU
#             mutaxasislik.strip(),   # Mutaxasislik
#             tel_no.strip(),         # Tel-no
#             doctor_name.strip(),    # Vrach ism-familiya
#             vaqt                    # Data
#         ]
        
#         # Save to YangiVrach sheet
#         spreadsheet = client.open("DoriXarajatlar")
#         yangi_vrach_sheet = spreadsheet.worksheet("YangiVrach")
#         await asyncio.to_thread(yangi_vrach_sheet.append_row, yangi_qator)
        
#         # Keshni tozalash: Yangi ma'lumotlar qo'shilganda keshni yangilash
#         global _cached_data
#         _cached_data = None
#         get_cached_sheets_data.cache_clear()
        
#         return {"success": True, "message": "✅ Янги врач муваффақиятли қўшилди!"}
        
#     except Exception as e:
#         return {"success": False, "message": f"Хатолик: {str(e)}"}

# @app.post("/save_data/")
# async def save_data(
#     ism: str = Form(...),
#     region: str = Form(...),
#     vrach: str = Form(...),
#     harajat_turi: str = Form(...),
#     apteka: str = Form(...),
#     summa_bonus: float = Form(...),
#     kompaniya_turi: str = Form(...),
#     izoh: str = Form(...),
#     username: str = Depends(authenticate)
# ):
#     """Optimized save function"""
#     data = get_cached_sheets_data()
#     if not data or not client:
#         return {"success": False, "message": "Google Sheets bilan bog'lanish xatosi"}
    
#     def find_exact_match(user_input, options):
#         user_input_norm = unidecode(user_input).lower().strip()
#         for opt in options:
#             if user_input_norm == unidecode(opt).lower().strip():
#                 return opt
#         return None
    
#     # Validate all required fields
#     if not all([ism.strip(), region.strip(), vrach.strip(), apteka.strip(), 
#                 harajat_turi.strip(), kompaniya_turi.strip(), izoh.strip()]):
#         return {"success": False, "message": "Барча мажбурий майдонларни тўлдириш керак!"}
    
#     if summa_bonus <= 0:
#         return {"success": False, "message": "Сумма бонус 0 дан катта бўлиш керак!"}
    
#     # Check exact matches - allow custom entries for names and regions from editable selects
#     vrach_match = find_exact_match(vrach, data['shifokorlar'])
#     apteka_match = find_exact_match(apteka, data['dorixonalar'])
    
#     # For ism and region, accept either exact match or custom entry
#     ism_match = find_exact_match(ism, data['ismlar']) or ism.strip()
#     region_match = find_exact_match(region, data['regionlar']) or region.strip()
    
#     if not vrach_match:
#         return {"success": False, "message": f"Врач номи рўйхатда топилмади: '{vrach}'. Тавсия этилган рўйхатдан танланг ёки тўғри киритинг!"}
#     if not apteka_match:
#         return {"success": False, "message": f"Аптека номи рўйхатда топилмади: '{apteka}'. Тавсия этилган рўйхатдан танланг ёки тўғри киритинг!"}
    
#     # Calculate month
#     if harajat_turi == "Аптека 100%":
#         oy = datetime.now().month
#     else:
#         hozirgi_oy = datetime.now().month
#         oy = hozirgi_oy + 1 if hozirgi_oy < 12 else 1
    
#     oy_nomi = calendar.month_name[oy]
#     oy_nomi_uz = {
#         "January": "Январ", "February": "Феврал", "March": "Март",
#         "April": "Апрел", "May": "Май", "June": "Июн",
#         "July": "Июл", "August": "Август", "September": "Сентябр",
#         "October": "Октябр", "November": "Ноябр", "December": "Декабр"
#     }[oy_nomi]
    
#     vaqt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     yangi_qator = [
#         ism_match, region_match, vaqt, vrach_match, harajat_turi,
#         apteka_match, summa_bonus, oy_nomi_uz, kompaniya_turi, izoh.strip()
#     ]
    
#     try:
#         spreadsheet = client.open("DoriXarajatlar")
#         kiritmalar_sheet = spreadsheet.worksheet("Kiritmalar")
#         await asyncio.to_thread(kiritmalar_sheet.append_row, yangi_qator)
        
#         # Keshni tozalash: Yangi ma'lumotlar qo'shilganda keshni yangilash
#         global _cached_data
#         _cached_data = None
#         get_cached_sheets_data.cache_clear()
        
#         return {"success": True, "message": "✅ Маълумот муваффақиятли сақланди!"}
#     except Exception as e:
#         return {"success": False, "message": f"Хатолик: {str(e)}"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8080)






from fastapi import FastAPI, Form, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import calendar
from unidecode import unidecode
import secrets
import os
import json
import asyncio
from functools import lru_cache
from typing import List, Optional

app = FastAPI()
security = HTTPBasic()

# Auth credentials
VALID_USERNAME = "MarketingPFL"
VALID_PASSWORD = "yordamkerak"

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    is_correct_username = secrets.compare_digest(credentials.username, VALID_USERNAME)
    is_correct_password = secrets.compare_digest(credentials.password, VALID_PASSWORD)
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

def get_google_credentials():
    try:
        creds_path = "credentials.json"
        SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file(creds_path, scopes=SCOPE)
        return gspread.authorize(creds)
    except Exception as e:
        print(f"Error getting credentials: {e}")
        return None

# Global variables with caching
client = None
_cached_data = None

@lru_cache(maxsize=1)
def get_cached_sheets_data():
    global client, _cached_data
    try:
        if not client:
            client = get_google_credentials()
        
        if client and not _cached_data:
            SPREADSHEET_NAME = "DoriXarajatlar"
            spreadsheet = client.open(SPREADSHEET_NAME)
            
            shifokorlar_sheet = spreadsheet.worksheet("Shifokorlar")
            dorixonalar_sheet = spreadsheet.worksheet("Dorixonalar")
            ismlar_sheet = spreadsheet.worksheet("IsmFamiliya")
            regionlar_sheet = spreadsheet.worksheet("Regionlar")
            # Yangi: Mutaxasisliklar sheetini qo'shish
            mutaxasisliklar_sheet = spreadsheet.worksheet("Mutaxasisliklar")
            
            shifokorlar = shifokorlar_sheet.col_values(1)[1:]
            dorixonalar = dorixonalar_sheet.col_values(1)[1:]
            ismlar = ismlar_sheet.col_values(1)[1:]
            regionlar = regionlar_sheet.col_values(1)[1:]
            # Yangi: Mutaxasisliklar ma'lumotlarini olish
            mutaxasisliklar = mutaxasisliklar_sheet.col_values(1)[1:]
            
            _cached_data = {
                'shifokorlar': shifokorlar,
                'dorixonalar': dorixonalar,
                'ismlar': ismlar,
                'regionlar': regionlar,
                'mutaxasisliklar': mutaxasisliklar # Yangi ma'lumot
            }
            
        return _cached_data
    except Exception as e:
        print(f"Error getting cached data: {e}")
        return None

def get_recommendations_fast(user_input: str, options: List[str], limit: int = 10) -> List[str]:
    if not user_input or len(user_input) < 1:
        return []
    
    user_input_norm = unidecode(user_input).lower()
    matches = []
    
    for opt in options:
        opt_norm = unidecode(opt).lower()
        if user_input_norm == opt_norm:
            return [opt]
        elif user_input_norm in opt_norm:
            score = len(user_input_norm) / len(opt_norm)
            matches.append((opt, score))
            
            if len(matches) >= limit * 2:
                break
    
    matches.sort(key=lambda x: x[1], reverse=True)
    return [match[0] for match in matches[:limit]]

# Yangi: Keshni davriy yangilash funksiyasi
async def refresh_cache_periodically():
    while True:
        print("Refreshing cached data...")
        get_cached_sheets_data.cache_clear() # Keshni tozalash
        data = get_cached_sheets_data() # Ma'lumotlarni qayta yuklash
        if data:
            print("✅ Cached data refreshed successfully")
        else:
            print("⚠️ Warning: Could not refresh Google Sheets data")
        await asyncio.sleep(300) # Har 5 daqiqada (300 soniya) yangilash

@app.on_event("startup")
async def startup_event():
    print("Initializing data...")
    data = get_cached_sheets_data()
    if data:
        print("✅ Data loaded successfully")
    else:
        print("⚠️ Warning: Could not initialize Google Sheets")
    
    # Keshni davriy yangilash vazifasini ishga tushirish
    asyncio.create_task(refresh_cache_periodically())

@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request, username: str = Depends(authenticate)):
    html_content = """
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>💊 Дори харажатлари</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 10px;
            }
            
            .container {
                max-width: 1000px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
                position: relative;
            }
            
            .header {
                background: linear-gradient(45deg, #667eea, #764ba2);
                color: white;
                padding: 20px;
                text-align: center;
                position: relative;
            }
            
            .sidebar-toggle {
                position: absolute;
                top: 50%;
                left: 20px;
                transform: translateY(-50%);
                background: rgba(255,255,255,0.2);
                border: none;
                color: white;
                padding: 10px;
                border-radius: 8px;
                cursor: pointer;
                font-size: 18px;
                transition: background 0.2s;
            }
            
            .sidebar-toggle:hover {
                background: rgba(255,255,255,0.3);
            }
            
            .sidebar {
                position: fixed;
                top: 0;
                left: -300px;
                width: 300px;
                height: 100vh;
                background: white;
                box-shadow: 2px 0 10px rgba(0,0,0,0.1);
                transition: left 0.3s ease;
                z-index: 2000;
                padding: 20px;
            }
            
            .sidebar.active {
                left: 0;
            }
            
            .sidebar-header {
                padding-bottom: 20px;
                border-bottom: 1px solid #eee;
                margin-bottom: 20px;
            }
            
            .sidebar-close {
                float: right;
                background: none;
                border: none;
                font-size: 24px;
                cursor: pointer;
                color: #666;
            }
            
            .sidebar-menu {
                list-style: none;
            }
            
            .sidebar-menu li {
                margin-bottom: 10px;
            }
            
            .sidebar-menu a {
                display: block;
                padding: 15px;
                text-decoration: none;
                color: #333;
                border-radius: 8px;
                transition: all 0.2s;
            }
            
            .sidebar-menu a:hover, .sidebar-menu a.active {
                background: #f8f9fa;
                color: #667eea;
            }
            
            .overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                background: rgba(0,0,0,0.5);
                z-index: 1500;
                display: none;
            }
            
            .overlay.active {
                display: block;
            }
            
            .content {
                padding: 30px;
            }
            
            .section {
                display: none;
            }
            
            .section.active {
                display: block;
            }
            
            .form-row {
                display: flex;
                gap: 15px;
                margin-bottom: 20px;
                flex-wrap: wrap;
            }
            
            .form-group {
                position: relative;
                flex: 1;
                min-width: 250px;
            }
            
            .form-group.full-width {
                flex: 100%;
                min-width: 100%;
            }
            
            label {
                display: block;
                margin-bottom: 8px;
                font-weight: 600;
                color: #333;
                font-size: 14px;
            }
            
            .required { color: #e74c3c; }
            
            input, select, textarea {
                width: 100%;
                padding: 12px;
                border: 2px solid #e1e5e9;
                border-radius: 8px;
                font-size: 16px;
                transition: border-color 0.2s;
                background-color: #fff;
            }
            
            /* Editable select styles */
            select[data-editable="true"] {
                background: white url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="12" height="8" viewBox="0 0 12 8"><path fill="%23666" d="M6 8L0 2h12z"/></svg>') no-repeat right 12px center;
                appearance: none;
                -webkit-appearance: none;
                -moz-appearance: none;
            }
            
            input:focus, select:focus, textarea:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
            }
            
            .suggestions {
                position: absolute;
                top: 100%;
                left: 0;
                right: 0;
                background: white;
                border: 1px solid #e1e5e9;
                border-top: none;
                border-radius: 0 0 8px 8px;
                max-height: 200px;
                overflow-y: auto;
                z-index: 1000;
                box-shadow: 0 4px 15px rgba(0,0,0,0.15);
                display: none;
            }
            
            .suggestion-item {
                padding: 12px;
                cursor: pointer;
                border-bottom: 1px solid #f1f1f1;
                transition: background-color 0.15s;
            }
            
            .suggestion-item:hover, .suggestion-item.active {
                background-color: #f8f9fa;
            }
            
            .suggestion-item:last-child { border-bottom: none; }
            
            .btn {
                background: linear-gradient(45deg, #667eea, #764ba2);
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
                transition: all 0.2s;
                font-weight: 600;
                min-width: 150px;
            }
            
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102,126,234,0.4);
            }
            
            .btn:active { transform: translateY(0); }
            
            .btn:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
            }
            
            .btn-secondary {
                background: linear-gradient(45deg, #28a745, #20c997);
            }
            
            .btn-secondary:hover {
                box-shadow: 0 5px 15px rgba(40,167,69,0.4);
            }
            
            .message {
                padding: 15px;
                margin: 15px 0;
                border-radius: 8px;
                font-weight: 500;
                display: none;
            }
            
            .success {
                background: #d4edda;
                color: #155724;
                border-left: 4px solid #28a745;
            }
            
            .error {
                background: #f8d7da;
                color: #721c24;
                border-left: 4px solid #dc3545;
            }
            
            .loading {
                display: none;
                text-align: center;
                padding: 20px;
            }
            
            .spinner {
                border: 3px solid #f3f3f3;
                border-top: 3px solid #667eea;
                border-radius: 50%;
                width: 30px;
                height: 30px;
                animation: spin 1s linear infinite;
                margin: 0 auto 10px;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .legend {
                background: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                margin-top: 20px;
                text-align: center;
                color: #666;
                font-size: 14px;
            }
            
            .search-indicator {
                position: absolute;
                right: 12px;
                top: 50%;
                transform: translateY(-50%);
                color: #666;
                font-size: 12px;
                display: none;
            }
            
            /* Mobile Responsive */
            @media (max-width: 768px) {
                body {
                    padding: 5px;
                }
                
                .container {
                    border-radius: 10px;
                }
                
                .header {
                    padding: 15px;
                }
                
                .header h1 {
                    font-size: 20px;
                    margin-top: 10px;
                }
                
                .content {
                    padding: 15px;
                }
                
                .form-row {
                    flex-direction: column;
                    gap: 10px;
                }
                
                .form-group {
                    min-width: 100%;
                }
                
                input, select, textarea {
                    font-size: 16px; /* Prevents zoom on iOS */
                    padding: 15px 12px;
                }
                
                .btn {
                    width: 100%;
                    padding: 18px;
                    font-size: 18px;
                }
                
                .sidebar {
                    width: 280px;
                }
                
                .sidebar-toggle {
                    left: 15px;
                    padding: 8px;
                }
            }
            
            @media (max-width: 480px) {
                .header h1 {
                    font-size: 18px;
                }
                
                .content {
                    padding: 10px;
                }
                
                .sidebar {
                    width: 100%;
                    left: -100%;
                }
            }
        </style>
    </head>
    <body>
        <!-- Sidebar -->
        <div id="sidebar" class="sidebar">
            <div class="sidebar-header">
                <h3>📋 Меню</h3>
                <button class="sidebar-close" onclick="toggleSidebar()">×</button>
            </div>
            <ul class="sidebar-menu">
                <li><a href="#" class="menu-item active" data-section="main-form">📊 Асосий форма</a></li>
                <li><a href="#" class="menu-item" data-section="add-doctor">👨‍⚕️ Янги врач қўшиш</a></li>
            </ul>
        </div>
        
        <div id="overlay" class="overlay" onclick="toggleSidebar()"></div>
        
        <div class="container">
            <div class="header">
                <button class="sidebar-toggle" onclick="toggleSidebar()">☰</button>
                <h1>💊 Маркетинг учун рўйхат</h1>
            </div>
            
            <div class="content">
                <!-- Main Form Section -->
                <div id="main-form" class="section active">
                    <form id="mainForm">
                        <div class="form-row">
                            <div class="form-group">
                                <label for="ism">👤 Исм-Фамилия <span class="required">*</span></label>
                                <select id="ism" name="ism" required data-editable="true">
                                    <option value="">Танланг ёки киритинг...</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="region">📍 Регион <span class="required">*</span></label>
                                <select id="region" name="region" required>
                                    <option value="">Танланг...</option>
                                </select>
                            </div>
                        </div>

                        <div class="form-row">
                            <div class="form-group">
                                <label for="vrach">👨‍⚕️ Врач <span class="required">*</span></label>
                                <input type="text" id="vrach" name="vrach" required autocomplete="off" 
                                       placeholder="Врач номини киритинг...">
                                <div class="search-indicator" id="vrach-indicator">🔍</div>
                                <div id="vrach-suggestions" class="suggestions"></div>
                            </div>
                            <div class="form-group">
                                <label for="harajat_turi">💼 Инвеститция тури <span class="required">*</span></label>
                                <select id="harajat_turi" name="harajat_turi" required>
                                    <option value="">Танланг...</option>
                                    <option value="Аптека 100%">Аптека 100%</option>
                                    <option value="Оптовик маркетинг 23%">Оптовик маркетинг 23%</option>
                                    <option value="Предоплата маркетинг">Предоплата маркетинг</option>
                                    <option value="Аванс маркетинг">Аванс маркетинг</option>
                                </select>
                            </div>
                        </div>

                        <div class="form-row">
                            <div class="form-group">
                                <label for="apteka">🏥 Аптека <span class="required">*</span></label>
                                <input type="text" id="apteka" name="apteka" required autocomplete="off"
                                       placeholder="Аптека номини киритинг...">
                                <div class="search-indicator" id="apteka-indicator">🔍</div>
                                <div id="apteka-suggestions" class="suggestions"></div>
                            </div>
                            <div class="form-group">
                                <label for="summa_bonus">💰 Сумма бонус <span class="required">*</span></label>
                                <input type="number" id="summa_bonus" name="summa_bonus" step="0.01" 
                                       min="0.01" required placeholder="0.00">
                            </div>
                        </div>

                        <div class="form-row">
                            <div class="form-group">
                                <label for="kompaniya_turi">🏢 Бренд <span class="required">*</span></label>
                                <select id="kompaniya_turi" name="kompaniya_turi" required>
                                    <option value="">Танланг...</option>
                                    <option value="GMX">GMX</option>
                                    <option value="BP">BP</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="izoh">📝 Изоҳ <span class="required">*</span></label>
                                <textarea id="izoh" name="izoh" rows="3" required 
                                          placeholder="Изоҳ киритинг..."></textarea>
                            </div>
                        </div>

                        <div style="text-align: center; margin-top: 30px;">
                            <button type="submit" class="btn" id="submitBtn">
                                ✅ Сақлаш
                            </button>
                        </div>
                    </form>
                </div>
                
                <!-- Add Doctor Section -->
                <div id="add-doctor" class="section">
                    <h2>👨‍⚕️ Янги врач қўшиш</h2>
                    <form id="doctorForm">
                        <div class="form-row">
                            <div class="form-group">
                                <label for="doctor_region">📍 Регион <span class="required">*</span></label>
                                <select id="doctor_region" name="doctor_region" required>
                                    <option value="">Танланг...</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="doctor_mp">👤 МП <span class="required">*</span></label>
                                <select id="doctor_mp" name="doctor_mp" required data-editable="true">
                                    <option value="">Танланг ёки киритинг...</option>
                                </select>
                            </div>
                        </div>
                        
                        <div class="form-row">
                            <div class="form-group">
                                <label for="dori_nomi">💊 Дори номи <span class="required">*</span></label>
                                <input type="text" id="dori_nomi" name="dori_nomi" required 
                                       placeholder="Дори номини киритинг...">
                            </div>
                            <div class="form-group">
                                <label for="lpu">🏥 ЛПУ <span class="required">*</span></label>
                                <input type="text" id="lpu" name="lpu" required 
                                       placeholder="ЛПУ номини киритинг...">
                            </div>
                        </div>
                        
                        <div class="form-row">
                            <div class="form-group">
                                <label for="mutaxasislik">🩺 Мутахассислик <span class="required">*</span></label>
                                <select id="mutaxasislik" name="mutaxasislik" required>
                                    <option value="">Танланг...</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="tel_no">📞 Телефон рақами <span class="required">*</span></label>
                                <input type="tel" id="tel_no" name="tel_no" required 
                                       placeholder="+998901234567">
                            </div>
                        </div>
                        
                        <div class="form-row">
                            <div class="form-group full-width">
                                <label for="doctor_name">👨‍⚕️ Врач исм-фамилияси <span class="required">*</span></label>
                                <input type="text" id="doctor_name" name="doctor_name" required 
                                       placeholder="Исм-фамилия киритинг...">
                            </div>
                        </div>
                        
                        <div style="text-align: center; margin-top: 30px;">
                            <button type="submit" class="btn btn-secondary" id="doctorSubmitBtn">
                                ➕ Врач қўшиш
                            </button>
                        </div>
                    </form>
                </div>
                
                <div id="loading" class="loading">
                    <div class="spinner"></div>
                    <p>Юкланмоқда...</p>
                </div>
                
                <div id="message" class="message"></div>
                
                <div class="legend">
                    <span class="required">*</span> - Мажбурий майдонлар
                </div>
            </div>
        </div>
        
        <script>
        // Global variables
        let debounceTimers = {};
        let cachedData = { doctors: [], pharmacies: [], names: [], regions: [], mutaxasisliklar: [] }; // mutaxasisliklar qo'shildi
        
        const elements = {
            ism: null, region: null, vrach: null, apteka: null,
            doctorRegion: null, doctorMp: null, mutaxasislik: null, // mutaxasislik qo'shildi
            vrachSuggestions: null, aptekaSuggestions: null,
            vrachIndicator: null, aptekaIndicator: null,
            form: null, doctorForm: null, message: null, loading: null,
            submitBtn: null, doctorSubmitBtn: null
        };
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            cacheElements();
            initializeData();
            setupEventListeners();
            setupEditableSelects();
        });
        
        function cacheElements() {
            elements.ism = document.getElementById('ism');
            elements.region = document.getElementById('region');
            elements.vrach = document.getElementById('vrach');
            elements.apteka = document.getElementById('apteka');
            elements.doctorRegion = document.getElementById('doctor_region');
            elements.doctorMp = document.getElementById('doctor_mp');
            elements.mutaxasislik = document.getElementById('mutaxasislik'); // mutaxasislik elementi
            elements.vrachSuggestions = document.getElementById('vrach-suggestions');
            elements.aptekaSuggestions = document.getElementById('apteka-suggestions');
            elements.vrachIndicator = document.getElementById('vrach-indicator');
            elements.aptekaIndicator = document.getElementById('apteka-indicator');
            elements.form = document.getElementById('mainForm');
            elements.doctorForm = document.getElementById('doctorForm');
            elements.message = document.getElementById('message');
            elements.loading = document.getElementById('loading');
            elements.submitBtn = document.getElementById('submitBtn');
            elements.doctorSubmitBtn = document.getElementById('doctorSubmitBtn');
        }
        
        async function initializeData() {
            try {
                await Promise.all([loadNames(), loadRegions(), loadMutaxasisliklar()]); // loadMutaxasisliklar() qo'shildi
                console.log('✅ Data loaded successfully');
            } catch (error) {
                console.error('❌ Error loading data:', error);
                showMessage('Маълумотлар юклашда хатолик юз берди', 'error');
            }
        }
        
        async function loadNames() {
            const response = await fetch('/get_names/');
            const data = await response.json();
            cachedData.names = data.names;
            
            // Clear existing options before adding new ones
            elements.ism.innerHTML = '<option value="">Танланг ёки киритинг...</option>';
            elements.doctorMp.innerHTML = '<option value="">Танланг ёки киритинг...</option>';

            // Load names for main form
            const fragment1 = document.createDocumentFragment();
            data.names.forEach(name => {
                const option = document.createElement('option');
                option.value = name;
                option.textContent = name;
                fragment1.appendChild(option);
            });
            elements.ism.appendChild(fragment1);
            
            // Load names for MP dropdown in doctor form
            const fragment2 = document.createDocumentFragment();
            data.names.forEach(name => {
                const option = document.createElement('option');
                option.value = name;
                option.textContent = name;
                fragment2.appendChild(option);
            });
            elements.doctorMp.appendChild(fragment2);
        }
        
        async function loadRegions() {
            const response = await fetch('/get_regions/');
            const data = await response.json();
            cachedData.regions = data.regions;

            // Clear existing options before adding new ones
            elements.region.innerHTML = '<option value="">Танланг...</option>';
            elements.doctorRegion.innerHTML = '<option value="">Танланг...</option>';
            
            // Load regions for main form
            const fragment1 = document.createDocumentFragment();
            data.regions.forEach(region => {
                const option = document.createElement('option');
                option.value = region;
                option.textContent = region;
                fragment1.appendChild(option);
            });
            elements.region.appendChild(fragment1);
            
            // Load regions for doctor form
            const fragment2 = document.createDocumentFragment();
            data.regions.forEach(region => {
                const option = document.createElement('option');
                option.value = region;
                option.textContent = region;
                fragment2.appendChild(option);
            });
            elements.doctorRegion.appendChild(fragment2);
        }

        // Yangi: Mutaxasisliklar ma'lumotlarini yuklash funksiyasi
        async function loadMutaxasisliklar() {
            const response = await fetch('/get_mutaxasisliklar/');
            const data = await response.json();
            cachedData.mutaxasisliklar = data.mutaxasisliklar;

            elements.mutaxasislik.innerHTML = '<option value="">Танланг...</option>';
            const fragment = document.createDocumentFragment();
            data.mutaxasisliklar.forEach(mutaxasislik => {
                const option = document.createElement('option');
                option.value = mutaxasislik;
                option.textContent = mutaxasislik;
                fragment.appendChild(option);
            });
            elements.mutaxasislik.appendChild(fragment);
        }
        
        function setupEditableSelects() {
            // Make selects with data-editable="true" behave like editable dropdowns
            document.querySelectorAll('select[data-editable="true"]').forEach(select => {
                // Create hidden input for custom values
                let hiddenInput = select.parentNode.querySelector(`input[name="${select.name}"]`);
                if (!hiddenInput) { // Create only if it doesn't exist
                    hiddenInput = document.createElement('input');
                    hiddenInput.type = 'hidden';
                    hiddenInput.name = select.name;
                    select.parentNode.insertBefore(hiddenInput, select.nextSibling);
                }
                
                // Handle select change
                select.addEventListener('change', function() {
                    hiddenInput.value = this.value;
                });
                
                // Allow typing by converting to input-like behavior
                select.addEventListener('keydown', function(e) {
                    if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey) { // Single character key, not a modifier
                        // Convert to searchable mode
                        this.setAttribute('data-search-mode', 'true');
                        this.style.color = '#666';
                        
                        // Create a temporary option for search
                        let searchOption = this.querySelector('option[data-search]');
                        if (!searchOption) {
                            searchOption = document.createElement('option');
                            searchOption.setAttribute('data-search', 'true');
                            searchOption.value = '';
                            this.insertBefore(searchOption, this.firstChild);
                        }
                        
                        searchOption.textContent = e.key;
                        searchOption.selected = true;
                        hiddenInput.value = e.key;
                        
                        // Prevent default select behavior
                        e.preventDefault();
                    }
                });
                
                // Handle further typing
                select.addEventListener('keyup', function(e) {
                    if (this.getAttribute('data-search-mode') === 'true') {
                        const searchOption = this.querySelector('option[data-search]');
                        if (searchOption) {
                            if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey) {
                                searchOption.textContent += e.key;
                                hiddenInput.value = searchOption.textContent;
                            } else if ((e.key === 'Backspace' || e.key === 'Delete')) {
                                let currentText = searchOption.textContent;
                                if (currentText.length > 0) {
                                    searchOption.textContent = currentText.slice(0, -1);
                                    hiddenInput.value = searchOption.textContent;
                                }
                            }
                        }
                    }
                });
                
                // Reset search mode on blur
                select.addEventListener('blur', function() {
                    this.removeAttribute('data-search-mode');
                    this.style.color = '';
                    const searchOption = this.querySelector('option[data-search]');
                    if (searchOption && searchOption.textContent.trim() === '') {
                        searchOption.remove();
                    } else if (searchOption) {
                        // If there's text in searchOption, make it the selected value
                        select.value = searchOption.textContent;
                        hiddenInput.value = searchOption.textContent;
                        searchOption.remove(); // Remove the temporary search option
                    }
                });

                // Ensure hidden input is updated on initial load if a value is pre-selected
                if (select.value) {
                    hiddenInput.value = select.value;
                }
            });
        }
        
        function setupEventListeners() {
            // Search functionality
            elements.vrach?.addEventListener('input', (e) => handleSearch(e, 'vrach'));
            elements.apteka?.addEventListener('input', (e) => handleSearch(e, 'apteka'));
            
            // Hide suggestions on outside click
            document.addEventListener('click', (e) => {
                if (!e.target.closest('.form-group')) {
                    hideSuggestions();
                }
            });
            
            // Form submissions
            elements.form?.addEventListener('submit', handleMainFormSubmit);
            elements.doctorForm?.addEventListener('submit', handleDoctorFormSubmit);
            
            // Menu navigation
            document.querySelectorAll('.menu-item').forEach(item => {
                item.addEventListener('click', (e) => {
                    e.preventDefault();
                    const section = e.target.dataset.section;
                    showSection(section);
                    
                    // Update active menu item
                    document.querySelectorAll('.menu-item').forEach(mi => mi.classList.remove('active'));
                    e.target.classList.add('active');
                    
                    // Close sidebar on mobile
                    if (window.innerWidth <= 768) {
                        toggleSidebar();
                    }
                });
            });
        }
        
        function toggleSidebar() {
            const sidebar = document.getElementById('sidebar');
            const overlay = document.getElementById('overlay');
            
            sidebar.classList.toggle('active');
            overlay.classList.toggle('active');
        }
        
        function showSection(sectionId) {
            document.querySelectorAll('.section').forEach(section => {
                section.classList.remove('active');
            });
            document.getElementById(sectionId).classList.add('active');
        }
        
        function handleSearch(e, type) {
            const value = e.target.value;
            const indicator = type === 'vrach' ? elements.vrachIndicator : elements.aptekaIndicator;
            
            clearTimeout(debounceTimers[type]);
            
            if (value.length >= 1) {
                indicator.style.display = 'block';
                debounceTimers[type] = setTimeout(() => {
                    performSearch(value, type);
                }, 200);
            } else {
                indicator.style.display = 'none';
                hideSuggestions(type);
            }
        }
        
        async function performSearch(query, type) {
            try {
                const endpoint = type === 'vrach' ? '/recommend_doctor/' : '/recommend_pharmacy/';
                const paramName = type === 'vrach' ? 'doctor_name' : 'pharmacy_name';
                
                const formData = new FormData();
                formData.append(paramName, query);
                
                const response = await fetch(endpoint, {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                displaySuggestions(type, data.recommendations);
                
            } catch (error) {
                console.error(`Search error for ${type}:`, error);
            } finally {
                const indicator = type === 'vrach' ? elements.vrachIndicator : elements.aptekaIndicator;
                indicator.style.display = 'none';
            }
        }
        
        function displaySuggestions(type, suggestions) {
            const container = type === 'vrach' ? elements.vrachSuggestions : elements.aptekaSuggestions;
            const input = type === 'vrach' ? elements.vrach : elements.apteka;
            
            container.innerHTML = '';
            
            if (suggestions.length === 0) {
                container.style.display = 'none';
                return;
            }
            
            const fragment = document.createDocumentFragment();
            suggestions.forEach(suggestion => {
                const div = document.createElement('div');
                div.className = 'suggestion-item';
                div.textContent = suggestion;
                div.addEventListener('click', () => {
                    input.value = suggestion;
                    hideSuggestions(type);
                });
                fragment.appendChild(div);
            });
            
            container.appendChild(fragment);
            container.style.display = 'block';
        }
        
        function hideSuggestions(type) {
            if (type) {
                const container = type === 'vrach' ? elements.vrachSuggestions : elements.aptekaSuggestions;
                container.style.display = 'none';
            } else {
                elements.vrachSuggestions.style.display = 'none';
                elements.aptekaSuggestions.style.display = 'none';
            }
        }
        
        // Main form submission
        async function handleMainFormSubmit(e) {
            e.preventDefault();
            
            elements.submitBtn.disabled = true;
            elements.submitBtn.textContent = '⏳ Сақланмоқда...';
            
            showLoading(true);
            hideMessage();
            
            const formData = new FormData(elements.form);
            
            // Handle editable selects
            const ismHidden = document.querySelector('input[name="ism"]');
            const regionHidden = document.querySelector('input[name="region"]');
            
            if (ismHidden && ismHidden.value) {
                formData.set('ism', ismHidden.value);
            }
            // For region, it's a standard select, so its value is already in formData
            // No need for regionHidden check unless it's also data-editable="true"
            // If region is also editable, uncomment the following:
            // if (regionHidden && regionHidden.value) {
            //     formData.set('region', regionHidden.value);
            // }
            
            try {
                const response = await fetch('/save_data/', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showMessage(result.message, 'success');
                    elements.form.reset();
                    elements.vrach.value = '';
                    elements.apteka.value = '';
                    hideSuggestions();
                    
                    // Reset editable selects' hidden inputs
                    document.querySelectorAll('select[data-editable="true"]').forEach(select => {
                        const hiddenInput = select.parentNode.querySelector(`input[name="${select.name}"]`);
                        if (hiddenInput) hiddenInput.value = '';
                        select.value = ''; // Reset the select itself
                    });

                    // Re-load names and regions to reflect potential new custom entries
                    await initializeData();

                } else {
                    showMessage(result.message, 'error');
                }
            } catch (error) {
                showMessage('Хатолик юз берди: ' + error.message, 'error');
            } finally {
                showLoading(false);
                elements.submitBtn.disabled = false;
                elements.submitBtn.textContent = '✅ Сақлаш';
            }
        }
        
        // Doctor form submission
        async function handleDoctorFormSubmit(e) {
            e.preventDefault();
            
            elements.doctorSubmitBtn.disabled = true;
            elements.doctorSubmitBtn.textContent = '⏳ Қўшилмоқда...';
            
            showLoading(true);
            hideMessage();
            
            const formData = new FormData(elements.doctorForm);
            
            // Handle editable selects for doctor form
            const mpHidden = document.querySelector('input[name="doctor_mp"]');
            if (mpHidden && mpHidden.value) {
                formData.set('doctor_mp', mpHidden.value);
            }
            
            try {
                const response = await fetch('/add_doctor/', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showMessage(result.message, 'success');
                    elements.doctorForm.reset();
                    
                    // Reset editable selects' hidden inputs
                    document.querySelectorAll('select[data-editable="true"]').forEach(select => {
                        const hiddenInput = select.parentNode.querySelector(`input[name="${select.name}"]`);
                        if (hiddenInput) hiddenInput.value = '';
                        select.value = ''; // Reset the select itself
                    });

                    // Re-load names and regions to reflect potential new custom entries
                    await initializeData();

                } else {
                    showMessage(result.message, 'error');
                }
            } catch (error) {
                showMessage('Хатолик юз берди: ' + error.message, 'error');
            } finally {
                showLoading(false);
                elements.doctorSubmitBtn.disabled = false;
                elements.doctorSubmitBtn.textContent = '➕ Врач қўшиш';
            }
        }
        
        function showMessage(text, type) {
            elements.message.textContent = text;
            elements.message.className = `message ${type}`;
            elements.message.style.display = 'block';
            
            if (type === 'success') {
                setTimeout(() => {
                    hideMessage();
                }, 5000);
            }
        }
        
        function hideMessage() {
            elements.message.style.display = 'none';
        }
        
        function showLoading(show) {
            elements.loading.style.display = show ? 'block' : 'none';
        }
        
        // Touch events for better mobile experience
        if ('ontouchstart' in window) {
            document.addEventListener('touchstart', function() {}, {passive: true});
        }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/get_names/")
async def get_names(username: str = Depends(authenticate)):
    """Fast cached names endpoint"""
    data = get_cached_sheets_data()
    return {"names": data['ismlar'] if data else []}

@app.get("/get_regions/")
async def get_regions(username: str = Depends(authenticate)):
    """Fast cached regions endpoint"""
    data = get_cached_sheets_data()
    return {"regions": data['regionlar'] if data else []}

# Yangi: Mutaxasisliklar ro'yxatini qaytarish uchun endpoint
@app.get("/get_mutaxasisliklar/")
async def get_mutaxasisliklar(username: str = Depends(authenticate)):
    """Fast cached mutaxasisliklar endpoint"""
    data = get_cached_sheets_data()
    return {"mutaxasisliklar": data['mutaxasisliklar'] if data else []}

@app.post("/recommend_doctor/")
async def recommend_doctor(doctor_name: str = Form(...), username: str = Depends(authenticate)):
    """Async doctor recommendations"""
    data = get_cached_sheets_data()
    if not data:
        return {"recommendations": []}
    
    recommendations = await asyncio.to_thread(
        get_recommendations_fast, doctor_name, data['shifokorlar']
    )
    return {"recommendations": recommendations}

@app.post("/recommend_pharmacy/")
async def recommend_pharmacy(pharmacy_name: str = Form(...), username: str = Depends(authenticate)):
    """Async pharmacy recommendations"""
    data = get_cached_sheets_data()
    if not data:
        return {"recommendations": []}
    
    recommendations = await asyncio.to_thread(
        get_recommendations_fast, pharmacy_name, data['dorixonalar']
    )
    return {"recommendations": recommendations}

@app.post("/add_doctor/")
async def add_doctor(
    doctor_region: str = Form(...),
    doctor_mp: str = Form(...),
    dori_nomi: str = Form(...),
    lpu: str = Form(...),
    mutaxasislik: str = Form(...), # Endi bu selectdan keladi
    tel_no: str = Form(...),
    doctor_name: str = Form(...),
    username: str = Depends(authenticate)
):
    """Add new doctor to YangiVrach sheet with new order"""
    if not client:
        return {"success": False, "message": "Google Sheets bilan bog'lanish xatosi"}
    
    # Validate all required fields
    if not all([doctor_region.strip(), doctor_mp.strip(), dori_nomi.strip(), 
                lpu.strip(), mutaxasislik.strip(), tel_no.strip(), doctor_name.strip()]):
        return {"success": False, "message": "Барча майдонларни тўлдириш керак!"}
    
    # Validate phone number format
    # Allow 9-digit numbers starting with 9, and prepend +998
    if not tel_no.startswith('+998'):
        if tel_no.startswith('9') and len(tel_no) == 9:
            tel_no = '+998' + tel_no
        else:
            return {"success": False, "message": "Телефон рақами нотўғри форматда! (+998901234567)"}
    
    try:
        # Prepare data with timestamp in the new order: Region, MP, Dori nomi, LPU, Mutaxasislik, Tel-no, Vrach ism-familiya, Data
        vaqt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        yangi_qator = [
            doctor_region.strip(),  # Region
            doctor_mp.strip(),      # MP
            dori_nomi.strip(),      # Dori nomi
            lpu.strip(),            # LPU
            mutaxasislik.strip(),   # Mutaxasislik
            tel_no.strip(),         # Tel-no
            doctor_name.strip(),    # Vrach ism-familiya
            vaqt                    # Data
        ]
        
        # Save to YangiVrach sheet
        spreadsheet = client.open("DoriXarajatlar")
        yangi_vrach_sheet = spreadsheet.worksheet("YangiVrach")
        await asyncio.to_thread(yangi_vrach_sheet.append_row, yangi_qator)
        
        # Keshni tozalash: Yangi ma'lumotlar qo'shilganda keshni yangilash
        global _cached_data
        _cached_data = None
        get_cached_sheets_data.cache_clear()
        
        return {"success": True, "message": "✅ Янги врач муваффақиятли қўшилди!"}
        
    except Exception as e:
        return {"success": False, "message": f"Хатолик: {str(e)}"}

@app.post("/save_data/")
async def save_data(
    ism: str = Form(...),
    region: str = Form(...),
    vrach: str = Form(...),
    harajat_turi: str = Form(...),
    apteka: str = Form(...),
    summa_bonus: float = Form(...),
    kompaniya_turi: str = Form(...),
    izoh: str = Form(...),
    username: str = Depends(authenticate)
):
    """Optimized save function"""
    data = get_cached_sheets_data()
    if not data or not client:
        return {"success": False, "message": "Google Sheets bilan bog'lanish xatosi"}
    
    def find_exact_match(user_input, options):
        user_input_norm = unidecode(user_input).lower().strip()
        for opt in options:
            if user_input_norm == unidecode(opt).lower().strip():
                return opt
        return None
    
    # Validate all required fields
    if not all([ism.strip(), region.strip(), vrach.strip(), apteka.strip(), 
                harajat_turi.strip(), kompaniya_turi.strip(), izoh.strip()]):
        return {"success": False, "message": "Барча мажбурий майдонларни тўлдириш керак!"}
    
    if summa_bonus <= 0:
        return {"success": False, "message": "Сумма бонус 0 дан катта бўлиш керак!"}
    
    # Check exact matches - allow custom entries for names and regions from editable selects
    vrach_match = find_exact_match(vrach, data['shifokorlar'])
    apteka_match = find_exact_match(apteka, data['dorixonalar'])
    
    # For ism and region, accept either exact match or custom entry
    ism_match = find_exact_match(ism, data['ismlar']) or ism.strip()
    region_match = find_exact_match(region, data['regionlar']) or region.strip()
    
    if not vrach_match:
        return {"success": False, "message": f"Врач номи рўйхатда топилмади: '{vrach}'. Тавсия этилган рўйхатдан танланг ёки тўғри киритинг!"}
    if not apteka_match:
        return {"success": False, "message": f"Аптека номи рўйхатда топилмади: '{apteka}'. Тавсия этилган рўйхатдан танланг ёки тўғри киритинг!"}
    
    # Calculate month
    if harajat_turi == "Аптека 100%":
        oy = datetime.now().month
    else:
        hozirgi_oy = datetime.now().month
        oy = hozirgi_oy + 1 if hozirgi_oy < 12 else 1
    
    oy_nomi = calendar.month_name[oy]
    oy_nomi_uz = {
        "January": "Январ", "February": "Феврал", "March": "Март",
        "April": "Апрел", "May": "Май", "June": "Июн",
        "July": "Июл", "August": "Август", "September": "Сентябр",
        "October": "Октябр", "November": "Ноябр", "December": "Декабр"
    }[oy_nomi]
    
    vaqt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    yangi_qator = [
        ism_match, region_match, vaqt, vrach_match, harajat_turi,
        apteka_match, summa_bonus, oy_nomi_uz, kompaniya_turi, izoh.strip()
    ]
    
    try:
        spreadsheet = client.open("DoriXarajatlar")
        kiritmalar_sheet = spreadsheet.worksheet("Kiritmalar")
        await asyncio.to_thread(kiritmalar_sheet.append_row, yangi_qator)
        
        # Keshni tozalash: Yangi ma'lumotlar qo'shilganda keshni yangilash
        global _cached_data
        _cached_data = None
        get_cached_sheets_data.cache_clear()
        
        return {"success": True, "message": "✅ Маълумот муваффақиятли сақланди!"}
    except Exception as e:
        return {"success": False, "message": f"Хатолик: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

