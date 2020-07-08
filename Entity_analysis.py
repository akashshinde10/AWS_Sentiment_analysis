import boto3

#document
s3BucketName = "bucket-name"
documentName = "image-name.jpg"

#read document content if image is stored on local computer
with open(documentName, 'rb') as document:
    imageBytes = bytearray(document.read())

#amazon textract client
textract = boto3.client('textract')

#call amazon textract
response = textract.detect_document_text(
    Document={
        'S3Object':{
            'Bucket': s3BucketName,
            'Name': documentName
        }
    })
# to obtain the image from s3_bucket use
# {'S3Object':{
    
#     'Bucket':'Bucket_name',
#     'name': 'name_of_iamge'
# }} 
# to obtain the image from local computer use
# {'Bytes' : source_bytes}
#print response

#plain text
print("\nText\n======")
text = ""
for item in response["Blocks"]:
    if item["BlockType"] == "LINE":
        print('\033[94m' + item["Text"] + '\033[0m')
        text = text + " " + item["Text"]

# Amazon Comprehend
comprehend = boto3.client('comprehend')

#detect sentiment
sentiment = comprehend.detect_sentiment(LanguageCode="en", Text=text)
print("\nSentiment\n========\n{}",format(sentiment.get('Sentiment')))

#detect entities
entities = comprehend.detect_entities(LanguageCode="en", Text=text)
print("\nEntities\n=======")
for entity in entities["Entities"]:
    print("{}\t=>\t{}".format(entity["Type"], entity["Text"]))
