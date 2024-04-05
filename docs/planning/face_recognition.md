# face recognition plan

## by demand 

### endpoints

- extract faces
  - accepts an image
  - returns faces and names per face
- remember face
  - gives a face a name, save in dedicated folder
  - decline if already remembers, give reason - especially if name differs
- forget face
  - delete face from folder

### similarit method
#### face_recognition library
start with th librqry itself 
maintain images locally
single image needed for recognition 

save images long term only if requested (this will be called if consent obtained)

#### rag
start with milvua-lite (supports python 3.6) for local rag
if fails, use pinecone
use voyageai as embeddings provide 

## in background
video stream, face_recognition library 
keep information only on known faces

### endpoints 
- who do I see now?
- save last x minutes video


