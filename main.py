
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import rec




class User(BaseModel):
    id: int
    singer: str 
    
    
app = FastAPI()

def update_user(sing,id):
    data = pd.read_csv("/lastfm-matrix-germany.csv",delimiter=',',encoding='latin-1')
    data[sing] = np.where(data["user"] == id, 1,0)
    data.to_csv('/file_name.csv', encoding='utf-8')   


@app.post("/user/")
async def create_user(user: User):
    id=user.id
    singer=user.singer
    update_user(singer,id)
    return {"message": f"Singer {singer} has been added successfully to user number {id}."}


@app.get("/{user_id}/recom_pop") 
async def recom ():
    recom1=rec.rec_pop()
    return[     
                {'Try to listen to this Most popular Artist'},
                {' & '.join(recom1)},
        ]



@app.get("/{user_id}/recom_rand") 
async def recom ():
    recom1=rec.rec_rand()
    return[     
                {'Today artists recommendations'},
                {' & '.join(recom1)},
        ]


@app.get("/{user_id}/recom_unk") 
async def recom (user_id):

    if(rec.vef_user(int(user_id))):
     
     recom1=rec.rec_unk(user_id)
     return[     
                {'customer_id: ', user_id},
                {'Try to listen to this Artists for the first Time '},
                {' & '.join(recom1)},
        ]
    
    else : return {"User doesn't exist"}


@app.get("/{user_id}/recom_sim") 
async def recom (user_id):

    if(rec.vef_user(int(user_id))):
     
     recom1=rec.rec_sim(int(user_id))
     return[     
                {'customer_id: ', user_id},
                {'You May Also Like These Artists '},
                {' & '.join(recom1)},
        ]
    else : return {"User doesn't exist"}
