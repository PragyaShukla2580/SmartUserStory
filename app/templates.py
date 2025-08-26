# Map keywords to code templates/snippets
STARTER_TEMPLATES = {
    "login": '''
# Flask/Python example for login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    # Validate user and password
    if authenticate(data['user'], data['password']):
        return jsonify({'status': 'success'}), 200
    return jsonify({'status': 'fail'}), 401
''',
    "test": '''
# Pytest skeleton
def test_example():
    assert True
''',
    "api": '''
# FastAPI endpoint example
from fastapi import APIRouter

router = APIRouter()

@router.get("/resource")
def read_resource():
    return {"result": "success"}
''',
    "endpoint": '''
# Create a generic endpoint
@app.route('/resource', methods=['GET'])
def get_resource():
    return {'result': 'ok'}
'''
}
