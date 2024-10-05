from supabase import create_client

url = "http://45.76.222.23:8000"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ewogICJyb2xlIjogImFub24iLAogICJpc3MiOiAic3VwYWJhc2UiLAogICJpYXQiOiAxNzI4MDU3NjAwLAogICJleHAiOiAxODg1ODI0MDAwCn0.Xf52RhaQ7n0CEDPhW12rGnPFN2qceYolZDyQ21Mk-y8"
supabase = create_client(url, key)
