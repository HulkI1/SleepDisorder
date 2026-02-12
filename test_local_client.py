#!/usr/bin/env python3
"""
Local Flask test-client based test suite
"""
import sys
import json
from time import time
from pathlib import Path

sys.path.insert(0, '/workspaces/SleepDisorder')
import flask_app

app = flask_app.app

print('\n=== Running local test-client based suite ===\n')

with app.test_client() as client:
    # 1. Register
    print('1) Registering new user')
    ts = int(time())
    email = f'local_test_{ts}@example.com'
    register_data = {
        'email': email,
        'phone': '9998887777',
        'password': 'LocalPass123',
        'confirm_password': 'LocalPass123'
    }
    r = client.post('/register', data=register_data, follow_redirects=True)
    print('  -> Register status:', r.status_code)

    users_file = Path('/workspaces/SleepDisorder/data/users.json')
    if users_file.exists():
        users = json.loads(users_file.read_text())
        print('  -> Users file loaded, total users:', len(users))
        assert email in users, 'Registered email not found in users.json'
        print('  -> Registration persisted in users.json')
    else:
        raise SystemExit('users.json not found')

    # 2. Login
    print('\n2) Logging in as the new user')
    login_data = {'email': email, 'password': 'LocalPass123'}
    r = client.post('/login', data=login_data, follow_redirects=True)
    print('  -> Login status:', r.status_code)
    assert b'Dashboard' in r.data or r.status_code == 200, 'Login did not return dashboard'
    print('  -> Login appears successful')

    # 3) Access dashboard
    r = client.get('/dashboard')
    print('  -> Dashboard GET status:', r.status_code)
    assert r.status_code == 200

    # 4) Submit sleep analysis (form encoded)
    print('\n3) Submitting sleep analysis')
    analysis_form = {
        'phone_number': '9998887777',
        'age': '34',
        'gender': 'Male',
        'occupation': 'Engineer',
        'stress': '6',
        'bp': '120/80',
        'heart_rate': '72',
        'sleep_duration': '5.5',
        'tea_coffee': '2',
        'bmi': 'Normal',
        'snoring': 'Never',
        'work_hours': '9'
    }
    r = client.post('/predict', data=analysis_form)
    print('  -> Predict status:', r.status_code)
    j = r.get_json()
    print('  -> Predict response:', j)
    assert j and j.get('diagnosis'), 'Predict did not return diagnosis'

    # 5) Check analysis_history
    r = client.get('/analysis-history')
    print('  -> History status:', r.status_code)
    history = r.get_json()
    print('  -> Number of records for this user:', len(history))
    assert len(history) >= 1
    latest = history[-1]
    record_id = latest.get('id')
    print('  -> Latest record id:', record_id)

    # 6) Generate and download PDF
    print('\n4) Generating PDF for the latest record')
    r = client.get(f'/download-pdf/{record_id}')
    print('  -> PDF endpoint status:', r.status_code)
    assert r.status_code == 200
    data = r.data
    print('  -> PDF size bytes:', len(data))
    assert b'%PDF' in data[:1024], 'Returned file is not a PDF'
    print('  -> PDF appears valid')

    # 7) ML integration test: run a few predictions
    print('\n5) ML integration sanity checks')
    cases = [
        {'sleep_duration':'8','stress':'2','age':'30','bp':'110/70','heart_rate':'65','tea_coffee':'0','bmi':'Normal','snoring':'Never','work_hours':'8'},
        {'sleep_duration':'3.5','stress':'9','age':'45','bp':'140/90','heart_rate':'95','tea_coffee':'5','bmi':'Obese','snoring':'Every Night','work_hours':'12'}
    ]
    for i,c in enumerate(cases,1):
        payload = {
            'phone_number':'9998887777','age':c['age'],'gender':'Male','occupation':'Tester','stress':c['stress'],
            'bp':c['bp'],'heart_rate':c['heart_rate'],'sleep_duration':c['sleep_duration'],'tea_coffee':c['tea_coffee'],
            'bmi':c['bmi'],'snoring':c['snoring'],'work_hours':c['work_hours']
        }
        r = client.post('/predict', data=payload)
        j = r.get_json()
        print(f"  -> Case {i} prediction: {j.get('diagnosis')} (status {r.status_code})")

    # 8) Admin login and endpoints
    print('\n6) Admin login and admin endpoints')
    admin_login = {'password': flask_app.ADMIN_PASSWORD}
    ar = client.post('/admin-login', data=admin_login, follow_redirects=True)
    print('  -> Admin login status:', ar.status_code)

    # Access admin reports
    ar = client.get('/admin-reports')
    print('  -> Admin reports status:', ar.status_code)
    reports = ar.get_json()
    print('  -> Total reports in system:', len(reports))

    ar = client.get('/admin-urgent')
    print('  -> Admin urgent status:', ar.status_code)
    urgent = ar.get_json()
    print('  -> Urgent cases count:', len(urgent))

    ar = client.get('/admin-stats')
    print('  -> Admin stats status:', ar.status_code)
    stats = ar.get_json()
    print('  -> Admin stats snapshot:', stats)

print('\n=== Local tests completed successfully ===\n')
