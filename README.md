# SA_jobs-AI
this Project encompasses strict saudi jobs offering and has scam detection advance robust algortim 


LATER @ PROD correct this in code ... 

 No authentication: Backend endpoints are completely open 
❌ Anyone can directly call http://your-backend:7070/jobs/ without any token
❌ The backend never validates the Cognito JWT token
❌ No Authorization: Bearer <token> check in FastAPI
👉 When the user logs in, **AWS Cognito gives them a JWT token**.  
👉 Every time the user calls your **API**, they send that token along.  
👉 The **API checks the token** to make sure it’s valid and belongs to that user.  

In simple terms: **Login once → get token → API uses that token to verify you.**

more sources :: 
I’ve noted that these platforms provide free APIs:
- RemoteOK.io
- Wellfound (AngelList)
- We Work Remotely


REFER:: 

`bge-small-en-v1.5`
 Qwen2.5‑0.5B