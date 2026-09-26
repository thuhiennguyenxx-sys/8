import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "bi_mat_quan_ly_may_tho_hospital_v2"

# Thư mục lưu tạm file
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Danh sách 44 máy thở chuẩn hóa cho bệnh viện
MACHINES_DATA = [
    # ICU Khu B
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
    # Nhiệt Đới
    {"department": "Nhiệt Đới", "model": "PB840", "serial": "3512210776"},
    {"department": "Nhiệt Đới", "model": "PB840", "serial": "3512211171"},
    {"department": "Nhiệt Đới", "model": "PB560", "serial": "4096600895"},
    {"department": "Nhiệt Đới", "model": "PB560", "serial": "4096600896"},
    # HS Ngoại TK
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
    # PTT Người Lớn
    {"department": "PTT Người Lớn", "model": "PB840", "serial": "3512152876"},
    {"department": "PTT Người Lớn", "model": "PB840", "serial": "3512152565"},
    {"department": "PTT Người Lớn", "model": "PB840", "serial": "3512152616"},
    {"department": "PTT Người Lớn", "model": "PB980", "serial": "35B2104679"},
    {"department": "PTT Người Lớn", "model": "PB980", "serial": "35B2104677"},
    {"department": "PTT Người Lớn", "model": "PB840", "serial": "3512152898"},
    # ICU Khu D
    {"department": "ICU Khu D", "model": "PB840", "serial": "3512201145"},
    {"department": "ICU Khu D", "model": "PB840", "serial": "3512201156"},
    {"department": "ICU Khu D", "model": "PB840", "serial": "3512201160"},
    {"department": "ICU Khu D", "model": "PB840", "serial": "3512191966"},
    {"department": "ICU Khu D", "model": "PB840", "serial": "3512152874"},
    {"department": "ICU Khu D", "model": "PB840", "serial": "3512152885"},
    {"department": "ICU Khu D", "model": "PB840", "serial": "3512202941"},
    # PTT Trẻ Em
    {"department": "PTT Trẻ Em", "model": "PB980", "serial": "35B2104673"},
    {"department": "PTT Trẻ Em", "model": "PB980", "serial": "35B2104657"},
    {"department": "PTT Trẻ Em", "model": "PB980", "serial": "35B1401604"},
    {"department": "PTT Trẻ Em", "model": "PB980", "serial": "35B1401531"},
    {"department": "PTT Trẻ Em", "model": "PB980", "serial": "35B2104615"},
    {"department": "PTT Trẻ Em", "model": "PB980", "serial": "35B2104648"}
]

@app.route('/')
def index():
    reports_list = []
    return render_template('index.html', machines=MACHINES_DATA, reports=reports_list)

@app.route('/submit', methods=['POST'])
def submit_inspection():
    flash("Đã tiếp nhận biên bản", "success")
    return redirect(url_for('index'))

@app.route('/approve/<int:report_id>')
def approve_report(report_id):
    flash(f"Đã duyệt biên bản #{report_id}!", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
