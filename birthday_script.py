import os
import pandas as pd
from datetime import datetime
from twilio.rest import Client

# 1. Setup Twilio Connection
client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])

def make_deep_voice_call(child_name, target_phone):
    # The 'Polly.Matthew' voice provides that deep, professional male tone
    twiml_content = f"""
    <Response>
        <Say voice="Polly.Matthew">
            Good morning. This is the Children Reading for a Change Initiative automated system. 
            Today is {child_name}'s birthday. 
            Please remember to celebrate with them and make their day special.
            The CRCi mission continues with you. Goodbye.
        </Say>
    </Response>
    """
    client.calls.create(
        twiml=twiml_content,
        to=target_phone,
        from_=os.environ['TWILIO_NUMBER']
    )
    print(f"Success: Call placed for {child_name}")

# 2. Check the Database
try:
    df = pd.read_csv('birthdays.csv')
    today = datetime.now().strftime("%m-%d")
    
    # Look for matches
    matches = df[df['Birthday'] == today]
    
    if not matches.empty:
        for _, row in matches.iterrows():
            make_deep_voice_call(row['Name'], os.environ['MY_PHONE_NUMBER'])
    else:
        print("No birthdays today. System standing by.")
except Exception as e:
    print(f"Error: {e}")
