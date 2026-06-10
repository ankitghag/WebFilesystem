from fastapi.concurrency import run_in_threadpool

class StorageService:
    def __init__(self, r2client, bucket):
        self.r2client= r2client
        self.bucket= bucket

    async def put_object(self, fkey,file):
        print("SPUTOBJ")
        return await run_in_threadpool(self.r2client.put_object,
            Bucket=self.bucket,
            Key=f"node_{fkey}",
            Body=file.file,
            ContentType=file.content_type)

    
    async def get_object(self, fkey):
        response = await run_in_threadpool(
            self.r2client.get_object,
            Bucket=self.bucket,
            Key=f"node_{fkey}"
        )
        return response["Body"].read()
        
    def get_presigned_url(self, fkey):
        key= f"node_{fkey}"
        purl= self.r2client.generate_presigned_url(
            ClientMethod="put_object", 
            Params={"Bucket":self.bucket, "Key": key},
            ExpiresIn= 36000)
        return purl