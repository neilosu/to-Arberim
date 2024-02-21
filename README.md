# vocabulary-backend

# start server
```bash
python3 main.py
```

## Example
- Get list 1 unit 1 all word_ids
    ```bash
    curl --location 'http://127.0.0.1:5000/db/execute' \
    --header 'Content-Type: application/json' \
    --data '{
        
        "query":"SELECT word_id FROM Meaning WHERE list = 1 AND unit = 1"
    }'
    ```