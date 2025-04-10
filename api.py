from google.generativeai import GenerativeModel, configure

# Replace with your actual API key
API_KEY = "AIzaSyBK8Cukatlb4VjsCqcmoeZhw8Ju-peRTTo"

# Configure the API key
configure(api_key=API_KEY)

# Initialize the model
model = GenerativeModel('gemini-1.5-pro')

# Generate content
try:
    response = model.generate_content("寫一個報菜名的相聲段子")
    print(response.text)
except Exception as e:
    print(f"An error occurred: {e}")
    print("Please ensure you have set the correct API key and have installed the required packages.")
