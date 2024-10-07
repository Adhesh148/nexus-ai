To run api gateway + lambda 
https://www.youtube.com/watch?v=AUQRyl1SNcU&t=688s



DynamoDB restore and backup
To backup dynamodb:
dynamodump -m backup -r local -s project_issues --host localhost --port 4566 --accessKey a --secretKey a
dynamodump -m backup -r local -s project_files --host localhost --port 4566 --accessKey a --secretKey a
dynamodump -m backup -r local -s project_templates --host localhost --port 4566 --accessKey a --secretKey a
dynamodump -m backup -r local -s projects --host localhost --port 4566 --accessKey a --secretKey a

To restore: 
dynamodump -m restore -r us-east-1 -s project_files --host localhost --port 4566 --accessKey a --secretKey a
dynamodump -m restore -r us-east-1 -s project_issues --host localhost --port 4566 --accessKey a --secretKey a
dynamodump -m restore -r us-east-1 -s project_templates --host localhost --port 4566 --accessKey a --secretKey a
dynamodump -m restore -r us-east-1 -s projects --host localhost --port 4566 --accessKey a --secretKey a