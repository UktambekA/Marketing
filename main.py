# # import streamlit as st
# # import gspread
# # from google.oauth2.service_account import Credentials
# # from datetime import datetime
# # import calendar
# # from unidecode import unidecode
# # import json

# # # Page config
# # st.set_page_config(
# #     page_title="💊 Дори харажатларини киритиш",
# #     page_icon="💊",
# #     layout="wide"
# # )

# # # Auth credentials
# # VALID_USERNAME = "marketingMP"
# # VALID_PASSWORD = "mpmarket"

# # def get_google_credentials():
# #     try:
# #         # Path to your credentials JSON file
# #         creds_path = "credentials.json"  # Put your JSON file in the same directory
# #         SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# #         creds = Credentials.from_service_account_file(creds_path, scopes=SCOPE)
# #         return gspread.authorize(creds)
# #     except Exception as e:
# #         st.error(f"Error getting credentials: {e}")
# #         return None

# # @st.cache_data
# # def initialize_sheets():
# #     """Initialize and cache sheet data"""
# #     try:
# #         client = get_google_credentials()
# #         if client:
# #             SPREADSHEET_NAME = "DoriXarajatlar"
# #             spreadsheet = client.open(SPREADSHEET_NAME)
            
# #             shifokorlar_sheet = spreadsheet.worksheet("Shifokorlar")
# #             dorixonalar_sheet = spreadsheet.worksheet("Dorixonalar")
# #             ismlar_sheet = spreadsheet.worksheet("IsmFamiliya")
# #             regionlar_sheet = spreadsheet.worksheet("Regionlar")
            
# #             shifokorlar = shifokorlar_sheet.col_values(1)[1:]
# #             dorixonalar = dorixonalar_sheet.col_values(1)[1:]
# #             ismlar = ismlar_sheet.col_values(1)[1:]
# #             regionlar = regionlar_sheet.col_values(1)[1:]
            
# #             return shifokorlar, dorixonalar, ismlar, regionlar, client
# #         return None, None, None, None, None
# #     except Exception as e:
# #         st.error(f"Error initializing sheets: {e}")
# #         return None, None, None, None, None

# # def get_recommendations(user_input, options, limit=10):
# #     """Returns top matching recommendations"""
# #     if not user_input or len(user_input) < 1:
# #         return []
    
# #     user_input_norm = unidecode(user_input).lower()
# #     matches = []
    
# #     for opt in options:
# #         opt_norm = unidecode(opt).lower()
# #         if user_input_norm in opt_norm:
# #             score = len(user_input_norm) / len(opt_norm)
# #             matches.append((opt, score))
    
# #     matches.sort(key=lambda x: x[1], reverse=True)
# #     return [match[0] for match in matches[:limit]]

# # def find_exact_match(user_input, options):
# #     """Find exact match in options"""
# #     user_input_norm = unidecode(user_input).lower().strip()
# #     for opt in options:
# #         if user_input_norm == unidecode(opt).lower().strip():
# #             return opt
# #     return None

# # def authenticate():
# #     """Simple authentication"""
# #     if 'authenticated' not in st.session_state:
# #         st.session_state.authenticated = False
    
# #     if not st.session_state.authenticated:
# #         st.title("🔐 Кириш")
        
# #         with st.form("login_form"):
# #             username = st.text_input("Фойдаланувчи номи")
# #             password = st.text_input("Парол", type="password")
# #             submitted = st.form_submit_button("Кириш")
            
# #             if submitted:
# #                 if username == VALID_USERNAME and password == VALID_PASSWORD:
# #                     st.session_state.authenticated = True
# #                     st.rerun()
# #                 else:
# #                     st.error("Нотўғри фойдаланувчи номи ёки парол!")
# #         return False
# #     return True

# # def main():
# #     if not authenticate():
# #         return
    
# #     # Header
# #     st.title("💊 Маркетинг учун рўйхат")
    
# #     # Initialize data
# #     if 'data_loaded' not in st.session_state:
# #         with st.spinner("Маълумотлар юкланмоқда..."):
# #             shifokorlar, dorixonalar, ismlar, regionlar, client = initialize_sheets()
# #             if all([shifokorlar, dorixonalar, ismlar, regionlar, client]):
# #                 st.session_state.shifokorlar = shifokorlar
# #                 st.session_state.dorixonalar = dorixonalar
# #                 st.session_state.ismlar = ismlar
# #                 st.session_state.regionlar = regionlar
# #                 st.session_state.client = client
# #                 st.session_state.data_loaded = True
# #             else:
# #                 st.error("Маълумотларни юклашда хатолик юз берди!")
# #                 return
    
# #     # Logout button
# #     if st.sidebar.button("Чиқиш"):
# #         st.session_state.authenticated = False
# #         st.rerun()
    
# #     # Initialize session state for inputs
# #     if 'vrach_input' not in st.session_state:
# #         st.session_state.vrach_input = ""
# #     if 'apteka_input' not in st.session_state:
# #         st.session_state.apteka_input = ""
# #     if 'selected_vrach' not in st.session_state:
# #         st.session_state.selected_vrach = ""
# #     if 'selected_apteka' not in st.session_state:
# #         st.session_state.selected_apteka = ""
    
# #     # Main form
# #     col1, col2 = st.columns(2)
    
# #     with col1:
# #         # Name selection (REQUIRED)
# #         ism = st.selectbox(
# #             "👤 Исм-Фамилия *",
# #             options=[""] + st.session_state.ismlar,
# #             index=0,
# #             help="Мажбурий майдон"
# #         )
        
# #         # Region selection (REQUIRED)
# #         region = st.selectbox(
# #             "📍 Регион *",
# #             options=[""] + st.session_state.regionlar,
# #             index=0,
# #             help="Мажбурий майдон"
# #         )
        
# #         # Doctor input with real-time recommendations (REQUIRED)
# #         st.markdown("**👨‍⚕️ Врач (лотин ёки крилл) *** ")
# #         vrach_input = st.text_input(
# #             "Врач номини киритинг:",
# #             value=st.session_state.vrach_input,
# #             key="vrach_text_input",
# #             help="Камида 2 та ҳарф киритинг",
# #             label_visibility="collapsed"
# #         )
        
# #         # Update session state
# #         if vrach_input != st.session_state.vrach_input:
# #             st.session_state.vrach_input = vrach_input
# #             st.session_state.selected_vrach = ""
        
# #         # Show doctor recommendations
# #         if vrach_input and len(vrach_input) >= 1:
# #             doctor_suggestions = get_recommendations(vrach_input, st.session_state.shifokorlar, limit=10)
# #             if doctor_suggestions:
# #                 selected_doctor = st.selectbox(
# #                     "📋 Тавсия этилган врачлар:",
# #                     options=["Танланг..."] + doctor_suggestions,
# #                     key="doctor_suggestions"
# #                 )
# #                 if selected_doctor and selected_doctor != "Танланг...":
# #                     st.session_state.selected_vrach = selected_doctor
# #                     st.session_state.vrach_input = selected_doctor
# #                     st.rerun()
        
# #         # Investment type (REQUIRED)
# #         harajat_turi = st.selectbox(
# #             "💼 Инвеститция тури *",
# #             options=[
# #                 "",
# #                 "Аптека 100%",
# #                 "Оптовик маркетинг 23%",
# #                 "Предоплата маркетинг",
# #                 "Аванс маркетинг"
# #             ],
# #             help="Мажбурий майдон"
# #         )
    
# #     with col2:
# #         # Pharmacy input with real-time recommendations (REQUIRED)
# #         st.markdown("**🏥 Аптека (лотин ёки крилл) *** ")
# #         apteka_input = st.text_input(
# #             "Аптека номини киритинг:",
# #             value=st.session_state.apteka_input,
# #             key="apteka_text_input",
# #             help="Камида 2 та ҳарф киритинг",
# #             label_visibility="collapsed"
# #         )
        
# #         # Update session state
# #         if apteka_input != st.session_state.apteka_input:
# #             st.session_state.apteka_input = apteka_input
# #             st.session_state.selected_apteka = ""
        
# #         # Show pharmacy recommendations
# #         if apteka_input and len(apteka_input) >= 1:
# #             pharmacy_suggestions = get_recommendations(apteka_input, st.session_state.dorixonalar, limit=10)
# #             if pharmacy_suggestions:
# #                 selected_pharmacy = st.selectbox(
# #                     "📋 Тавсия этилган аптекалар:",
# #                     options=["Танланг..."] + pharmacy_suggestions,
# #                     key="pharmacy_suggestions"
# #                 )
# #                 if selected_pharmacy and selected_pharmacy != "Танланг...":
# #                     st.session_state.selected_apteka = selected_pharmacy
# #                     st.session_state.apteka_input = selected_pharmacy
# #                     st.rerun()
        
# #         # Bonus amount (REQUIRED)
# #         summa_bonus = st.number_input(
# #             "💰 Сумма бонус *",
# #             min_value=0.01,
# #             step=0.01,
# #             format="%.2f",
# #             help="Мажбурий майдон, 0 дан катта бўлиши керак"
# #         )
        
# #         # Company type (REQUIRED)
# #         kompaniya_turi = st.selectbox(
# #             "🏢 Бренд *",
# #             options=["", "GMX", "BP"],
# #             help="Мажбурий майдон"
# #         )
        
# #         # Comment (REQUIRED)
# #         izoh = st.text_area(
# #             "📝 Изоҳ *", 
# #             height=100,
# #             help="Мажбурий майдон"
# #         )
    
# #     # Get final values
# #     final_vrach = st.session_state.selected_vrach if st.session_state.selected_vrach else st.session_state.vrach_input
# #     final_apteka = st.session_state.selected_apteka if st.session_state.selected_apteka else st.session_state.apteka_input
    
# #     # Submit button
# #     if st.button("✅ Сақлаш", use_container_width=True, type="primary"):
# #         # Validation
# #         if not all([ism, region, final_vrach.strip(), final_apteka.strip(), harajat_turi, kompaniya_turi, izoh.strip()]):
# #             missing_fields = []
# #             if not ism: missing_fields.append("Исм-Фамилия")
# #             if not region: missing_fields.append("Регион")
# #             if not final_vrach.strip(): missing_fields.append("Врач")
# #             if not final_apteka.strip(): missing_fields.append("Аптека")
# #             if not harajat_turi: missing_fields.append("Инвеститция тури")
# #             if not kompaniya_turi: missing_fields.append("Бренд")
# #             if not izoh.strip(): missing_fields.append("Изоҳ")
            
# #             st.error(f"❌ Қуйидаги мажбурий майдонларни тўлдиринг: {', '.join(missing_fields)}")
# #             return
        
# #         if summa_bonus <= 0:
# #             st.error("❌ Сумма бонус 0 дан катта бўлиш керак!")
# #             return
        
# #         # Check exact matches
# #         vrach_match = find_exact_match(final_vrach, st.session_state.shifokorlar)
# #         apteka_match = find_exact_match(final_apteka, st.session_state.dorixonalar)
# #         ism_match = find_exact_match(ism, st.session_state.ismlar)
# #         region_match = find_exact_match(region, st.session_state.regionlar)
        
# #         if not all([vrach_match, apteka_match, ism_match, region_match]):
# #             missing = []
# #             if not ism_match: missing.append("Исм-Фамилия")
# #             if not region_match: missing.append("Регион")
# #             if not vrach_match: missing.append("Врач")
# #             if not apteka_match: missing.append("Аптека")
# #             st.error(f"❌ Қуйидагилар рўйхатда топилмади: {', '.join(missing)}")
# #             st.info("💡 Тавсия: Тавсия этилган рўйхатдан танланг ёки аниқ номни киритинг")
# #             return
        
# #         # Calculate month
# #         if harajat_turi == "Аптека 100%":
# #             oy = datetime.now().month
# #         else:
# #             hozirgi_oy = datetime.now().month
# #             oy = hozirgi_oy + 1 if hozirgi_oy < 12 else 1
        
# #         oy_nomi = calendar.month_name[oy]
# #         oy_nomi_uz = {
# #             "January": "Январ", "February": "Феврал", "March": "Март",
# #             "April": "Апрел", "May": "Май", "June": "Июн",
# #             "July": "Июл", "August": "Август", "September": "Сентябr",
# #             "October": "Октябр", "November": "Ноябр", "December": "Декабр"
# #         }[oy_nomi]
        
# #         # Prepare data
# #         vaqt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# #         yangi_qator = [
# #             ism_match, region_match, vaqt, vrach_match, harajat_turi,
# #             apteka_match, summa_bonus, oy_nomi_uz, kompaniya_turi, izoh.strip()
# #         ]
        
# #         # Save to Google Sheets
# #         try:
# #             with st.spinner("Маълумот сақланмоқда..."):
# #                 spreadsheet = st.session_state.client.open("DoriXarajatlar")
# #                 kiritmalar_sheet = spreadsheet.worksheet("Kiritmalar")
# #                 kiritmalar_sheet.append_row(yangi_qator)
# #                 st.success("✅ Маълумот муваффақиятли сақланди!")
                
# #                 # Clear inputs after successful save
# #                 st.session_state.vrach_input = ""
# #                 st.session_state.apteka_input = ""
# #                 st.session_state.selected_vrach = ""
# #                 st.session_state.selected_apteka = ""
# #                 st.rerun()
                
# #         except Exception as e:
# #             st.error(f"❌ Хатолик: {str(e)}")
    
# #     # Required field legend
# #     st.markdown("---")
# #     st.markdown("***** - Мажбурий майдонлар")

# # if __name__ == "__main__":




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
# VALID_USERNAME = "marketingMP"
# VALID_PASSWORD = "mpmarket"

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
#         # Path to your credentials JSON file
#         creds_path = "credentials.json"  # Put your JSON file in the same directory
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
#     """Cache Google Sheets data for faster access"""
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
#     """Faster recommendation function with optimizations"""
#     if not user_input or len(user_input) < 1:
#         return []
    
#     user_input_norm = unidecode(user_input).lower()
#     matches = []
    
#     # Early break for exact matches
#     for opt in options:
#         opt_norm = unidecode(opt).lower()
#         if user_input_norm == opt_norm:
#             return [opt]  # Exact match found, return immediately
#         elif user_input_norm in opt_norm:
#             score = len(user_input_norm) / len(opt_norm)
#             matches.append((opt, score))
            
#             # Early break if we have enough good matches
#             if len(matches) >= limit * 2:
#                 break
    
#     matches.sort(key=lambda x: x[1], reverse=True)
#     return [match[0] for match in matches[:limit]]

# @app.on_event("startup")
# async def startup_event():
#     """Initialize data on startup"""
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
#         <title>💊 Дори харажатлари - Optimized</title>
#         <style>
#             * { margin: 0; padding: 0; box-sizing: border-box; }
#             body {
#                 font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#                 background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#                 min-height: 100vh; padding: 20px;
#             }
#             .container {
#                 max-width: 900px; margin: 0 auto; background: white;
#                 border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
#                 overflow: hidden;
#             }
#             .header {
#                 background: linear-gradient(45deg, #667eea, #764ba2);
#                 color: white; padding: 30px; text-align: center;
#             }
#             .form-container { padding: 30px; }
#             .form-row { display: flex; gap: 20px; margin-bottom: 20px; }
#             .form-group { position: relative; flex: 1; }
#             .form-group.full-width { flex: 100%; }
#             label { 
#                 display: block; margin-bottom: 8px; font-weight: 600; 
#                 color: #333; font-size: 14px;
#             }
#             .required { color: #e74c3c; }
#             input, select, textarea {
#                 width: 100%; padding: 12px; border: 2px solid #e1e5e9;
#                 border-radius: 8px; font-size: 16px; transition: border-color 0.2s;
#                 background-color: #fff;
#             }
#             input:focus, select:focus, textarea:focus {
#                 outline: none; border-color: #667eea; box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
#             }
#             .suggestions {
#                 position: absolute; top: 100%; left: 0; right: 0;
#                 background: white; border: 1px solid #e1e5e9; border-top: none;
#                 border-radius: 0 0 8px 8px; max-height: 200px; overflow-y: auto;
#                 z-index: 1000; box-shadow: 0 4px 15px rgba(0,0,0,0.15);
#                 display: none;
#             }
#             .suggestion-item {
#                 padding: 12px; cursor: pointer; border-bottom: 1px solid #f1f1f1;
#                 transition: background-color 0.15s;
#             }
#             .suggestion-item:hover, .suggestion-item.active { 
#                 background-color: #f8f9fa; 
#             }
#             .suggestion-item:last-child { border-bottom: none; }
#             .btn {
#                 background: linear-gradient(45deg, #667eea, #764ba2);
#                 color: white; padding: 15px 40px; border: none;
#                 border-radius: 8px; font-size: 16px; cursor: pointer;
#                 transition: all 0.2s; font-weight: 600;
#                 min-width: 150px;
#             }
#             .btn:hover { 
#                 transform: translateY(-2px); 
#                 box-shadow: 0 5px 15px rgba(102,126,234,0.4);
#             }
#             .btn:active { transform: translateY(0); }
#             .btn:disabled {
#                 opacity: 0.6; cursor: not-allowed; transform: none;
#             }
#             .message { 
#                 padding: 15px; margin: 15px 0; border-radius: 8px; 
#                 font-weight: 500; display: none;
#             }
#             .success { 
#                 background: #d4edda; color: #155724; 
#                 border-left: 4px solid #28a745;
#             }
#             .error { 
#                 background: #f8d7da; color: #721c24; 
#                 border-left: 4px solid #dc3545;
#             }
#             .loading { 
#                 display: none; text-align: center; padding: 20px; 
#             }
#             .spinner {
#                 border: 3px solid #f3f3f3; border-top: 3px solid #667eea;
#                 border-radius: 50%; width: 30px; height: 30px;
#                 animation: spin 1s linear infinite; margin: 0 auto 10px;
#             }
#             @keyframes spin { 
#                 0% { transform: rotate(0deg); } 
#                 100% { transform: rotate(360deg); } 
#             }
#             .legend {
#                 background: #f8f9fa; padding: 15px; border-radius: 8px;
#                 margin-top: 20px; text-align: center; color: #666;
#                 font-size: 14px;
#             }
#             .search-indicator {
#                 position: absolute; right: 12px; top: 50%;
#                 transform: translateY(-50%); color: #666;
#                 font-size: 12px; display: none;
#             }
#         </style>
#     </head>
#     <body>
#         <div class="container">
#             <div class="header">
#                 <h1>💊 Маркетинг учун рўйхат</h1>
#             </div>
#             <div class="form-container">
#                 <form id="mainForm">
#                     <div class="form-row">
#                         <div class="form-group">
#                             <label for="ism">👤 Исм-Фамилия <span class="required">*</span></label>
#                             <select id="ism" name="ism" required>
#                                 <option value="">Танланг...</option>
#                             </select>
#                         </div>
#                         <div class="form-group">
#                             <label for="region">📍 Регион <span class="required">*</span></label>
#                             <select id="region" name="region" required>
#                                 <option value="">Танланг...</option>
#                             </select>
#                         </div>
#                     </div>

#                     <div class="form-row">
#                         <div class="form-group">
#                             <label for="vrach">👨‍⚕️ Врач <span class="required">*</span></label>
#                             <input type="text" id="vrach" name="vrach" required autocomplete="off" 
#                                    placeholder="Врач номини киритинг...">
#                             <div class="search-indicator" id="vrach-indicator">🔍</div>
#                             <div id="vrach-suggestions" class="suggestions"></div>
#                         </div>
#                         <div class="form-group">
#                             <label for="harajat_turi">💼 Инвеститция тури <span class="required">*</span></label>
#                             <select id="harajat_turi" name="harajat_turi" required>
#                                 <option value="">Танланг...</option>
#                                 <option value="Аптека 100%">Аптека 100%</option>
#                                 <option value="Оптовик маркетинг 23%">Оптовик маркетинг 23%</option>
#                                 <option value="Предоплата маркетинг">Предоплата маркетинг</option>
#                                 <option value="Аванс маркетинг">Аванс маркетинг</option>
#                             </select>
#                         </div>
#                     </div>

#                     <div class="form-row">
#                         <div class="form-group">
#                             <label for="apteka">🏥 Аптека <span class="required">*</span></label>
#                             <input type="text" id="apteka" name="apteka" required autocomplete="off"
#                                    placeholder="Аптека номини киритинг...">
#                             <div class="search-indicator" id="apteka-indicator">🔍</div>
#                             <div id="apteka-suggestions" class="suggestions"></div>
#                         </div>
#                         <div class="form-group">
#                             <label for="summa_bonus">💰 Сумма бонус <span class="required">*</span></label>
#                             <input type="number" id="summa_bonus" name="summa_bonus" step="0.01" 
#                                    min="0.01" required placeholder="0.00">
#                         </div>
#                     </div>

#                     <div class="form-row">
#                         <div class="form-group">
#                             <label for="kompaniya_turi">🏢 Бренд <span class="required">*</span></label>
#                             <select id="kompaniya_turi" name="kompaniya_turi" required>
#                                 <option value="">Танланг...</option>
#                                 <option value="GMX">GMX</option>
#                                 <option value="BP">BP</option>
#                             </select>
#                         </div>
#                         <div class="form-group">
#                             <label for="izoh">📝 Изоҳ <span class="required">*</span></label>
#                             <textarea id="izoh" name="izoh" rows="3" required 
#                                       placeholder="Изоҳ киритинг..."></textarea>
#                         </div>
#                     </div>

#                     <div style="text-align: center; margin-top: 30px;">
#                         <button type="submit" class="btn" id="submitBtn">
#                             ✅ Сақлаш
#                         </button>
#                     </div>
#                 </form>
                
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
#         // Optimized JavaScript with better performance
#         let debounceTimers = {};
#         let cachedData = {
#             doctors: [],
#             pharmacies: [],
#             names: [],
#             regions: []
#         };
        
#         // Faster DOM queries
#         const elements = {
#             ism: null,
#             region: null,
#             vrach: null,
#             apteka: null,
#             vrachSuggestions: null,
#             aptekaSuggestions: null,
#             vrachIndicator: null,
#             aptekaIndicator: null,
#             form: null,
#             message: null,
#             loading: null,
#             submitBtn: null
#         };
        
#         // Initialize DOM elements
#         document.addEventListener('DOMContentLoaded', function() {
#             // Cache DOM elements
#             elements.ism = document.getElementById('ism');
#             elements.region = document.getElementById('region');
#             elements.vrach = document.getElementById('vrach');
#             elements.apteka = document.getElementById('apteka');
#             elements.vrachSuggestions = document.getElementById('vrach-suggestions');
#             elements.aptekaSuggestions = document.getElementById('apteka-suggestions');
#             elements.vrachIndicator = document.getElementById('vrach-indicator');
#             elements.aptekaIndicator = document.getElementById('apteka-indicator');
#             elements.form = document.getElementById('mainForm');
#             elements.message = document.getElementById('message');
#             elements.loading = document.getElementById('loading');
#             elements.submitBtn = document.getElementById('submitBtn');
            
#             initializeData();
#             setupEventListeners();
#         });
        
#         // Load initial data with error handling
#         async function initializeData() {
#             try {
#                 await Promise.all([
#                     loadNames(),
#                     loadRegions()
#                 ]);
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
            
#             // Faster DOM manipulation
#             const fragment = document.createDocumentFragment();
#             data.names.forEach(name => {
#                 const option = document.createElement('option');
#                 option.value = name;
#                 option.textContent = name;
#                 fragment.appendChild(option);
#             });
#             elements.ism.appendChild(fragment);
#         }
        
#         async function loadRegions() {
#             const response = await fetch('/get_regions/');
#             const data = await response.json();
#             cachedData.regions = data.regions;
            
#             const fragment = document.createDocumentFragment();
#             data.regions.forEach(region => {
#                 const option = document.createElement('option');
#                 option.value = region;
#                 option.textContent = region;
#                 fragment.appendChild(option);
#             });
#             elements.region.appendChild(fragment);
#         }
        
#         function setupEventListeners() {
#             // Optimized search with debouncing
#             elements.vrach.addEventListener('input', (e) => handleSearch(e, 'vrach'));
#             elements.apteka.addEventListener('input', (e) => handleSearch(e, 'apteka'));
            
#             // Hide suggestions on outside click
#             document.addEventListener('click', (e) => {
#                 if (!e.target.closest('.form-group')) {
#                     hideSuggestions();
#                 }
#             });
            
#             // Form submission
#             elements.form.addEventListener('submit', handleSubmit);
#         }
        
#         function handleSearch(e, type) {
#             const value = e.target.value;
#             const indicator = type === 'vrach' ? elements.vrachIndicator : elements.aptekaIndicator;
            
#             // Clear previous timer
#             clearTimeout(debounceTimers[type]);
            
#             if (value.length >= 1) {
#                 indicator.style.display = 'block';
                
#                 // Debounce for 200ms
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
            
#             // Clear previous suggestions
#             container.innerHTML = '';
            
#             if (suggestions.length === 0) {
#                 container.style.display = 'none';
#                 return;
#             }
            
#             // Create suggestions fragment for better performance
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
        
#         async function handleSubmit(e) {
#             e.preventDefault();
            
#             // Disable submit button
#             elements.submitBtn.disabled = true;
#             elements.submitBtn.textContent = '⏳ Сақланмоқда...';
            
#             showLoading(true);
#             hideMessage();
            
#             const formData = new FormData(elements.form);
            
#             try {
#                 const response = await fetch('/save_data/', {
#                     method: 'POST',
#                     body: formData
#                 });
                
#                 const result = await response.json();
                
#                 if (result.success) {
#                     showMessage(result.message, 'success');
#                     elements.form.reset();
                    
#                     // Clear search inputs
#                     elements.vrach.value = '';
#                     elements.apteka.value = '';
#                     hideSuggestions();
#                 } else {
#                     showMessage(result.message, 'error');
#                 }
#             } catch (error) {
#                 showMessage('Хатолик юз берди: ' + error.message, 'error');
#             } finally {
#                 showLoading(false);
                
#                 // Re-enable submit button
#                 elements.submitBtn.disabled = false;
#                 elements.submitBtn.textContent = '✅ Сақлаш';
#             }
#         }
        
#         function showMessage(text, type) {
#             elements.message.textContent = text;
#             elements.message.className = `message ${type}`;
#             elements.message.style.display = 'block';
            
#             // Auto hide success messages
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
    
#     # Run recommendations in thread pool for better performance
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
    
#     # Check exact matches
#     vrach_match = find_exact_match(vrach, data['shifokorlar'])
#     apteka_match = find_exact_match(apteka, data['dorixonalar'])
#     ism_match = find_exact_match(ism, data['ismlar'])
#     region_match = find_exact_match(region, data['regionlar'])
    
#     if not all([vrach_match, apteka_match, ism_match, region_match]):
#         missing = []
#         if not ism_match: missing.append("Исм-Фамилия")
#         if not region_match: missing.append("Регион")
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
#         # Async Google Sheets operation
#         spreadsheet = client.open("DoriXarajatlar")
#         kiritmalar_sheet = spreadsheet.worksheet("Kiritmalar")
#         await asyncio.to_thread(kiritmalar_sheet.append_row, yangi_qator)
        
#         return {"success": True, "message": "✅ Маълумот муваффақиятли сақланди!"}
#     except Exception as e:
#         return {"success": False, "message": f"Хатолик: {str(e)}"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


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
VALID_USERNAME = "marketingMP"
VALID_PASSWORD = "mpmarket"

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
            
            shifokorlar = shifokorlar_sheet.col_values(1)[1:]
            dorixonalar = dorixonalar_sheet.col_values(1)[1:]
            ismlar = ismlar_sheet.col_values(1)[1:]
            regionlar = regionlar_sheet.col_values(1)[1:]
            
            _cached_data = {
                'shifokorlar': shifokorlar,
                'dorixonalar': dorixonalar,
                'ismlar': ismlar,
                'regionlar': regionlar
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

@app.on_event("startup")
async def startup_event():
    print("Initializing data...")
    data = get_cached_sheets_data()
    if data:
        print("✅ Data loaded successfully")
    else:
        print("⚠️ Warning: Could not initialize Google Sheets")

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
                                <select id="ism" name="ism" required>
                                    <option value="">Танланг...</option>
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
                                <label for="doctor_name">👤 Врач исм-фамилияси <span class="required">*</span></label>
                                <input type="text" id="doctor_name" name="doctor_name" required 
                                       placeholder="Исм-фамилия киритинг...">
                            </div>
                            <div class="form-group">
                                <label for="mutaxasislik">🩺 Мутахассислик <span class="required">*</span></label>
                                <input type="text" id="mutaxasislik" name="mutaxasislik" required 
                                       placeholder="Мутахассислик киритинг...">
                            </div>
                        </div>
                        
                        <div class="form-row">
                            <div class="form-group">
                                <label for="lpu">🏥 ЛПУ <span class="required">*</span></label>
                                <input type="text" id="lpu" name="lpu" required 
                                       placeholder="ЛПУ номини киритинг...">
                            </div>
                            <div class="form-group">
                                <label for="tel_no">📞 Телефон рақами <span class="required">*</span></label>
                                <input type="tel" id="tel_no" name="tel_no" required 
                                       placeholder="+998901234567">
                            </div>
                        </div>
                        
                        <div class="form-row">
                            <div class="form-group full-width">
                                <label for="dori_nomi">💊 Дори номи <span class="required">*</span></label>
                                <input type="text" id="dori_nomi" name="dori_nomi" required 
                                       placeholder="Дори номини киритинг...">
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
        let cachedData = { doctors: [], pharmacies: [], names: [], regions: [] };
        
        const elements = {
            ism: null, region: null, vrach: null, apteka: null,
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
        });
        
        function cacheElements() {
            elements.ism = document.getElementById('ism');
            elements.region = document.getElementById('region');
            elements.vrach = document.getElementById('vrach');
            elements.apteka = document.getElementById('apteka');
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
                await Promise.all([loadNames(), loadRegions()]);
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
            
            const fragment = document.createDocumentFragment();
            data.names.forEach(name => {
                const option = document.createElement('option');
                option.value = name;
                option.textContent = name;
                fragment.appendChild(option);
            });
            elements.ism.appendChild(fragment);
        }
        
        async function loadRegions() {
            const response = await fetch('/get_regions/');
            const data = await response.json();
            cachedData.regions = data.regions;
            
            const fragment = document.createDocumentFragment();
            data.regions.forEach(region => {
                const option = document.createElement('option');
                option.value = region;
                option.textContent = region;
                fragment.appendChild(option);
            });
            elements.region.appendChild(fragment);
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
            
            try {
                const response = await fetch('/add_doctor/', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showMessage(result.message, 'success');
                    elements.doctorForm.reset();
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
    doctor_name: str = Form(...),
    mutaxasislik: str = Form(...),
    lpu: str = Form(...),
    tel_no: str = Form(...),
    dori_nomi: str = Form(...),
    username: str = Depends(authenticate)
):
    """Add new doctor to YangiVrach sheet"""
    if not client:
        return {"success": False, "message": "Google Sheets bilan bog'lanish xatosi"}
    
    # Validate all required fields
    if not all([doctor_name.strip(), mutaxasislik.strip(), lpu.strip(), 
                tel_no.strip(), dori_nomi.strip()]):
        return {"success": False, "message": "Барча майдонларни тўлдириш керак!"}
    
    # Validate phone number format
    if not tel_no.startswith('+998') and not tel_no.startswith('998'):
        if tel_no.startswith('9') and len(tel_no) == 9:
            tel_no = '+998' + tel_no
        else:
            return {"success": False, "message": "Телефон рақами нотўғри форматда! (+998901234567)"}
    
    try:
        # Prepare data with timestamp
        vaqt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        yangi_qator = [
            doctor_name.strip(),
            mutaxasislik.strip(), 
            lpu.strip(),
            tel_no.strip(),
            dori_nomi.strip(),
            vaqt
        ]
        
        # Save to YangiVrach sheet
        spreadsheet = client.open("DoriXarajatlar")
        yangi_vrach_sheet = spreadsheet.worksheet("YangiVrach")
        await asyncio.to_thread(yangi_vrach_sheet.append_row, yangi_qator)
        
        # Clear cache to reload data (optional - for immediate updates)
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
        return {"success": False, "message": "Google Sheets bilan bog'lanish xatoli"}
    
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
    
    # Check exact matches
    vrach_match = find_exact_match(vrach, data['shifokorlar'])
    apteka_match = find_exact_match(apteka, data['dorixonalar'])
    ism_match = find_exact_match(ism, data['ismlar'])
    region_match = find_exact_match(region, data['regionlar'])
    
    if not all([vrach_match, apteka_match, ism_match, region_match]):
        missing = []
        if not ism_match: missing.append("Исм-Фамилия")
        if not region_match: missing.append("Регион")
        if not vrach_match: missing.append("Врач")
        if not apteka_match: missing.append("Аптека")
        return {"success": False, "message": f"Қуйидагилар рўйхатда топилмади: {', '.join(missing)}. Тавсия этилган рўйхатдан танланг!"}
    
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
        
        return {"success": True, "message": "✅ Маълумот муваффақиятли сақланди!"}
    except Exception as e:
        return {"success": False, "message": f"Хатолик: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
