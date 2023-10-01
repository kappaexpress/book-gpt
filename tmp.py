import openai
import pandas as pd
from datetime import datetime
import key

openai.api_key = key.api_key

# OpenAIが提供するモデル一覧取得
model_list = openai.Model.list().data
model_num  = len(model_list)

# リスト
created_at_list           = []
model_id_list             = []
allow_create_engine_list  = []
allow_fine_tuning_list    = []
allow_logprobs_list       = []
allow_sampling_list       = []
allow_search_indices_list = []
allow_view_list           = []


for i in range(model_num):
    # データ取得 
    created_at           = datetime.fromtimestamp(model_list[i].created)
    model_id             = model_list[i].id
    allow_create_engine  = model_list[i].permission[0].allow_create_engine
    allow_fine_tuning    = model_list[i].permission[0].allow_fine_tuning
    allow_logprobs       = model_list[i].permission[0].allow_logprobs
    allow_sampling       = model_list[i].permission[0].allow_sampling
    allow_search_indices = model_list[i].permission[0].allow_search_indices
    allow_view           = model_list[i].permission[0].allow_view 
    
    # 格納
    created_at_list.append(created_at)
    model_id_list.append(model_id)
    allow_create_engine_list.append(allow_create_engine)
    allow_fine_tuning_list.append(allow_fine_tuning)
    allow_logprobs_list.append(allow_logprobs)
    allow_sampling_list.append(allow_sampling)
    allow_search_indices_list.append(allow_search_indices)
    allow_view_list.append(allow_view)
    
# データフレーム
df = pd.DataFrame({
        "作成日":                  created_at_list,
        "モデルID":                model_id_list,
        "エンジンの作成許可":        allow_create_engine_list,
        "ファインチューニングの許可": allow_fine_tuning_list,
        "ログ確率の許可":           allow_logprobs_list,
        "サンプリングの許可":        allow_sampling_list,
        "検索インデックスの許可":     allow_search_indices_list,
        "ビューの許可":             allow_view_list,
                })

# 並び替え
df = df.sort_values("作成日", ascending=False).reset_index(drop=True)

print(df[["作成日", "モデルID"]])