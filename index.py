import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = "bi_mat_quan_ly_may_tho_hospital_v2"

# Cấu hình kết nối Supabase (đã dùng khóa anon chuẩn dạng eyJ...)
SUPABASE_URL = "https://sbxfxhkynfgoslhboqtt.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNieGZ4aGt5bmZnb3NsaGJvcXR0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTA0MzI4NDksImV4cCI6MjEwNjAwODg0OX0.Vl7_URmPVTGdS2G3QMkkyDZzdVXumd8KSEwnfCCq9So" # Dán khóa anon chuẩn của bạn vào đây

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    supabase = None

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

MACHINES_DATA = [
    {"department": "ICU Khu B", "model": "PB980", "serial": "35B1701595"},
    {"department": "ICU Khu B", "model": "PB840", "serial": "3512201164"},
    {"department": "ICU Khu B", "model": "PB840", "serial": "3512201151"},
    {"department": "ICU Khu B", "model": "PB980", "serial": "35B2005876"},
    {"department": "ICU Khu B", "model": "PB980", "serial": "35B2005879"},
    {"department": "ICU Khu B", "model": "PB980", "serial": "35B2104680"},
    {"department": "ICU Khu B", "model": "PB840", "serial": "3512201144"},
    {"department": "ICU Khu B", "model": "PB980", "serial": "35B2104496"},
    {"department": "ICU Khu B", "model": "PB980", "serial": "35B2104459"},
    {"department": "ICU Khu B", "model": "PB840", "serial": "35B2005882"},
    {"department": "ICU Khu B", "model": "PB840", "serial": "35B2005880"},
    {"department": "Nhiệt Đới", "model": "PB840", "serial": "3512210776"},
    {"department": "Nhiệt Đới", "model": "PB840", "serial": "3512211171"},
    {"department": "Nhiệt Đới", "model": "PB560", "serial": "4096600895"},
    {"department": "Nhiệt Đới", "model": "PB560", "serial": "4096600896"},
    {"department": "HS Ngoại TK", "model": "PB560", "serial": "4096600905"},
    {"department": "HS Ngoại TK", "model": "PB840", "serial": "3512211582"},
    {"department": "HS Ngoại TK", "model": "PB840", "serial": "3512211576"},
    {"department": "HS Ngoại TK", "model": "PB840", "serial": "3512211573"},
    {"department": "HS Ngoại TK", "model": "PB840", "serial": "3512211561"},
    {"department": "HS Ngoại TK", "model": "PB840", "serial": "3512211564"},
    {"department": "HS Ngoại TK", "model": "PB840", "serial": "3512211559"},
    {"department": "HS Ngoại TK", "model": "PB840", "serial": "3512211555"},
    {"department": "HS Ngoại TK", "model": "PB840", "serial": "3512211547"},
    {"department": "HS Ngoại TK", "model": "PB840", "serial": "3512211565"},
    {"department": "PTT Người Lớn", "model": "PB840", "serial": "3512152876"},
    {"department": "PTT Người Lớn", "model": "PB840", "serial": "3512152565"},
    {"department": "PTT Người Lớn", "model": "PB840", "serial": "3512152616"},
    {"department": "PTT Người Lớn", "model": "PB980", "serial": "35B2104679"},
    {"department": "PTT Người Lớn", "model": "PB980", "serial": "35B2104677"},
    {"department": "PTT Người Lớn", "model": "PB840", "serial": "3512152898"},
    {"department": "ICU Khu D", "model": "PB840", "serial": "3512201145"},
    {"department": "ICU Khu D", "model": "PB840", "serial": "3512201156"},
    {"department": "ICU Khu D", "model": "PB840", "serial": "3512201160"},
    {"department": "ICU Khu D", "model": "PB840", "serial": "3512191966"},
    {"department": "ICU Khu D", "model": "PB840", "serial": "3512152874"},
    {"department": "ICU Khu D", "model": "PB840", "serial": "3512152885"},
    {"department": "ICU Khu D", "model": "PB840", "serial": "3512202941"},
    {"department": "PTT Trẻ Em", "model": "PB980", "serial": "35B2104673"},
    {"department": "PTT Trẻ Em", "model": "PB980", "serial": "35B2104657"},
    {"department": "PTT Trẻ Em", "model": "PB980", "serial": "35B1401604"},
    {"department": "PTT Trẻ Em", "model": "PB980", "serial": "35B1401531"},
    {"department": "PTT Trẻ Em", "model": "PB980", "serial": "35B2104615"},
    {"department": "PTT Trẻ Em", "model": "PB980", "serial": "35B2104648"}
]

@app.route('/')
def index():
    rows = []
    if supabase:
        try:
            response = supabase.table('reports').select('*').order('id', desc=True).execute()
            rows = response.data
        except Exception as e:
            print("Lỗi DB:", e)

    reports_list = []
    for r in rows:
        media_str = r.get('media_list', '')
        media_files = media_str.split(',') if media_str else []
        
        names = (r.get('parts_name') or "").split(';;;')
        codes = (r.get('parts_code') or "").split(';;;')
        qtys = (r.get('parts_qty') or "").split(';;;')
        
        parts_combined = []
        for i in range(max(len(names), len(codes), len(qtys))):
            p_name = names[i] if i < len(names) else ""
            p_code = codes[i] if i < len(codes) else ""
            p_qty = qtys[i] if i < len(qtys) else ""
            if p_name or p_code or p_qty:
                parts_combined.append({"name": p_name, "code": p_code, "qty": p_qty})

        reports_list.append({
            "id": r.get('id'),
            "engineer": r.get('engineer'),
            "department": r.get('department'),
            "model": r.get('model'),
            "serial": r.get('serial'),
            "notes": r.get('notes'),
            "has_replacement": bool(r.get('has_replacement')),
            "parts_list": parts_combined,
            "media_list": [m for m in media_files if m],
            "status": r.get('status'),
            "created_at": r.get('created_at') or "N/A"
        })

    return render_template('index.html', machines=MACHINES_DATA, reports=reports_list)

@app.route('/submit', methods=['POST'])
def submit_inspection():
    engineer_name = request.form.get('engineer_name')
    machine_info = request.form.get('machine_serial')
    notes = request.form.get('notes')
    has_replacement = 1 if request.form.get('has_replacement') == 'on' else 0
    
    parts_names = request.form.getlist('parts_name[]')
    parts_codes = request.form.getlist('parts_code[]')
    parts_qtys = request.form.getlist('parts_qty[]')

    parts_name_str = ";;;".join(parts_names)
    parts_code_str = ";;;".join(parts_codes)
    parts_qty_str = ";;;".join(parts_qtys)

    created_at = datetime.now().strftime('%d/%m/%Y %H:%M')

    media_filenames = []
    files = request.files.getlist('media_files')
    for file in files:
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            media_filenames.append(filename)

    media_str = ",".join(media_filenames)

    parts = machine_info.split(' | ')
    dept = parts[0] if len(parts) > 0 else ""
    model = parts[1] if len(parts) > 1 else ""
    serial = parts[2] if len(parts) > 2 else ""

    status = "Chờ duyệt xuất kho linh kiện" if has_replacement == 1 else "Đã hoàn tất kiểm tra định kỳ"

    if supabase:
        try:
            supabase.table('reports').insert({
                "engineer": engineer_name,
                "department": dept,
                "model": model,
                "serial": serial,
                "notes": notes,
                "has_replacement": has_replacement,
                "parts_name": parts_name_str,
                "parts_code": parts_code_str,
                "parts_qty": parts_qty_str,
                "media_list": media_str,
                "status": status,
                "created_at": created_at
            }).execute()
            flash("Đã lưu biên bản thành công!", "success")
        except Exception as e:
            flash(f"Lỗi lưu DB: {e}", "danger")

    return redirect(url_for('index'))

@app.route('/approve/<int:report_id>')
def approve_report(report_id):
    if supabase:
        try:
            supabase.table('reports').update({
                "status": "Đã duyệt xuất kho & Hoàn tất"
            }).eq('id', report_id).execute()
            flash(f"Đã duyệt biên bản #{report_id}!", "success")
        except Exception as e:
            flash(f"Lỗi duyệt: {e}", "danger")
    return redirect(url_for('index'))
    if __name__ == '__main__':
    app.run(debug=True)
