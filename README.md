# linto-platform-nlp-extractive-summarization

## Description
This repository is for building a Docker image for LinTO's NLP service: Extractive Summarization on the basis of [linto-platform-nlp-core](https://github.com/linto-ai/linto-platform-nlp-core), can be deployed along with [LinTO stack](https://github.com/linto-ai/linto-platform-stack) or in a standalone way (see Develop section in below).

LinTo's NLP services adopt the basic design concept of spaCy: [component and pipeline](https://spacy.io/usage/processing-pipelines), components (located under the folder `components/`) are decoupled from the service and can be easily re-used in other spaCy projects, components are organised into pipelines for realising specific NLP tasks. 

This service can be launched in two ways: REST API and Celery task, with and without GPU support.

## Usage

See documentation : [https://doc.linto.ai](https://doc.linto.ai)

## Deploy

With our proposed stack [https://github.com/linto-ai/linto-platform-stack](https://github.com/linto-ai/linto-platform-stack)

# Develop

## Build and run
1 Download models into `./assets` on the host machine (can be stored in other places), make sure that `git-lfs`: [Git Large File Storage](https://git-lfs.github.com/) is installed and availble at `/usr/local/bin/git-lfs`.
```bash
cd linto-platform-nlp-extractive-summarization/
bash scripts/download_models.sh
```

2 configure running environment variables
```bash
cp .envdefault .env
```

| Environment Variable | Description | Default Value |
| --- | --- | --- |
| `APP_LANG` | A space-separated list of supported languages for the application | fr en |
| `ASSETS_PATH_ON_HOST` | The path to the assets folder on the host machine | ./assets |
| `ASSETS_PATH_IN_CONTAINER` | The volume mount point of models in container | /app/assets |
| `LM_MAP` | A JSON string that maps each supported language to its corresponding language model | {"fr":"sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2","en":"sentence-transformers/all-MiniLM-L6-v2"} |
| `SERVICE_MODE` | The mode in which the service is served, either "http" (REST API) or "task" (Celery task) | "http" |
| `CONCURRENCY` | The maximum number of requests that can be handled concurrently | 1 |
| `USE_GPU` | A flag indicating whether to use GPU for computation or not, either "True" or "False" | True |
| `SERVICE_NAME` | The name of the micro-service | extsumm |
| `SERVICES_BROKER` | The URL of the broker server used for communication between micro-services | "redis://localhost:6379" |
| `BROKER_PASS` | The password for accessing the broker server | None |

4 Build image
```bash
sudo docker build --tag lintoai/linto-platform-nlp-extractive-summarization:latest .
```
or
```bash
sudo docker-compose build
```

5 Run container with GPU support, make sure that [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#installing-on-ubuntu-and-debian) and GPU driver are installed.
```bash
sudo docker run --gpus all \
--rm -p 80:80 \
-v $PWD/assets:/app/assets:ro \
--env-file .env \
lintoai/linto-platform-nlp-extractive-summarization:latest
```
<details>
  <summary>Check running with CPU only setting</summary>
  
  - remove `--gpus all` from the first command.
  - set `USE_GPU=False` in the `.env`.
</details>

or

```bash
sudo docker-compose up
```
<details>
  <summary>Check running with CPU only setting</summary>
  
  - remove `runtime: nvidia` from the `docker-compose.yml` file.
  - set `USE_GPU=False` in the `.env`.
</details>


6 If running under `SERVICE_MODE=http`, navigate to `http://localhost/docs` or `http://localhost/redoc` in your browser, to explore the REST API interactively. See the examples for how to query the API.


## Specification for `http://localhost/extsumm/{lang}`

### Supported languages
| {lang} | Model | Size |
| --- | --- | --- |
| `en` | [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) | 80 MB |
| `fr` | [sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2) | 418 MB |

### Request
Please use `" | "` (with a white-space on the left and right side) to seperate the segments (e.g., sentences, paragraphs, documents, etc.), which will be considered as the units for extractive summarization.
```json
{
  "articles": [
    {
      "text": "The Chrysler Building, the famous art deco New York skyscraper, will be sold for a small fraction of its previous sales price. | The deal, first reported by The Real Deal, was for $150 million, according to a source familiar with the deal. | Mubadala, an Abu Dhabi investment fund, purchased 90% of the building for $800 million in 2008. | Real estate firm Tishman Speyer had owned the other 10%. | The buyer is RFR Holding, a New York real estate company. | Officials with Tishman and RFR did not immediately respond to a request for comments. | It's unclear when the deal will close. | The building sold fairly quickly after being publicly placed on the market only two months ago. | The sale was handled by CBRE Group. | The incentive to sell the building at such a huge loss was due to the soaring rent the owners pay to Cooper Union, a New York college, for the land under the building. | The rent is rising from $7.75 million last year to $32.5 million this year to $41 million in 2028. | Meantime, rents in the building itself are not rising nearly that fast. | While the building is an iconic landmark in the New York skyline, it is competing against newer office towers with large floor-to-ceiling windows and all the modern amenities. | Still the building is among the best known in the city, even to people who have never been to New York. | It is famous for its triangle-shaped, vaulted windows worked into the stylized crown, along with its distinctive eagle gargoyles near the top. | It has been featured prominently in many films, including Men in Black 3, Spider-Man, Armageddon, Two Weeks Notice and Independence Day. | The previous sale took place just before the 2008 financial meltdown led to a plunge in real estate prices. | Still there have been a number of high profile skyscrapers purchased for top dollar in recent years, including the Waldorf Astoria hotel, which Chinese firm Anbang Insurance purchased in 2016 for nearly $2 billion, and the Willis Tower in Chicago, which was formerly known as Sears Tower, once the world's tallest. | Blackstone Group (BX) bought it for $1.3 billion 2015. | The Chrysler Building was the headquarters of the American automaker until 1953, but it was named for and owned by Chrysler chief Walter Chrysler, not the company itself. | Walter Chrysler had set out to build the tallest building in the world, a competition at that time with another Manhattan skyscraper under construction at 40 Wall Street at the south end of Manhattan. He kept secret the plans for the spire that would grace the top of the building, building it inside the structure and out of view of the public until 40 Wall Street was complete. | Once the competitor could rise no higher, the spire of the Chrysler building was raised into view, giving it the title."
    },
    {
      "text": "Junk foods taste good that’s why it is mostly liked by everyone of any age group especially kids and school going children. | They generally ask for the junk food daily because they have been trend so by their parents from the childhood. | They never have been discussed by their parents about the harmful effects of junk foods over health. | According to the research by scientists, it has been found that junk foods have negative effects on the health in many ways. | They are generally fried food found in the market in the packets. | They become high in calories, high in cholesterol, low in healthy nutrients, high in sodium mineral, high in sugar, starch, unhealthy fat, lack of protein and lack of dietary fibers. | Processed and junk foods are the means of rapid and unhealthy weight gain and negatively impact the whole body throughout the life. | It makes able a person to gain excessive weight which is called as obesity. | Junk foods tastes good and looks good however do not fulfil the healthy calorie requirement of the body. | Some of the foods like french fries, fried foods, pizza, burgers, candy, soft drinks, baked goods, ice cream, cookies, etc are the example of high-sugar and high-fat containing foods. | It is found according to the Centres for Disease Control and Prevention that Kids and children eating junk food are more prone to the type-2 diabetes. | In type-2 diabetes our body become unable to regulate blood sugar level. | Risk of getting this disease is increasing as one become more obese or overweight. | It increases the risk of kidney failure. | Eating junk food daily lead us to the nutritional deficiencies in the body because it is lack of essential nutrients, vitamins, iron, minerals and dietary fibers. | It increases risk of cardiovascular diseases because it is rich in saturated fat, sodium and bad cholesterol. | High sodium and bad cholesterol diet increases blood pressure and overloads the heart functioning. | One who like junk food develop more risk to put on extra weight and become fatter and unhealthier. | Junk foods contain high level carbohydrate which spike blood sugar level and make person more lethargic, sleepy and less active and alert. | Reflexes and senses of the people eating this food become dull day by day thus they live more sedentary life. | Junk foods are the source of constipation and other disease like diabetes, heart ailments, clogged arteries, heart attack, strokes, etc because of being poor in nutrition. | Junk food is the easiest way to gain unhealthy weight. | The amount of fats and sugar in the food makes you gain weight rapidly. | However, this is not a healthy weight. | It is more of fats and cholesterol which will have a harmful impact on your health. | Junk food is also one of the main reasons for the increase in obesity nowadays.This food only looks and tastes good, other than that, it has no positive points. | The amount of calorie your body requires to stay fit is not fulfilled by this food. | For instance, foods like French fries, burgers, candy, and cookies, all have high amounts of sugar and fats. | Therefore, this can result in long-term illnesses like diabetes and high blood pressure. | This may also result in kidney failure. | Above all, you can get various nutritional deficiencies when you don’t consume the essential nutrients, vitamins, minerals and more. | You become prone to cardiovascular diseases due to the consumption of bad cholesterol and fat plus sodium. | In other words, all this interferes with the functioning of your heart. | Furthermore, junk food contains a higher level of carbohydrates. | It will instantly spike your blood sugar levels. | This will result in lethargy, inactiveness, and sleepiness. | A person reflex becomes dull overtime and they lead an inactive life. | To make things worse, junk food also clogs your arteries and increases the risk of a heart attack. | Therefore, it must be avoided at the first instance to save your life from becoming ruined.The main problem with junk food is that people don’t realize its ill effects now. | When the time comes, it is too late. | Most importantly, the issue is that it does not impact you instantly. | It works on your overtime; you will face the consequences sooner or later. | Thus, it is better to stop now.You can avoid junk food by encouraging your children from an early age to eat green vegetables. | Their taste buds must be developed as such that they find healthy food tasty. | Moreover, try to mix things up. | Do not serve the same green vegetable daily in the same style. | Incorporate different types of healthy food in their diet following different recipes. | This will help them to try foods at home rather than being attracted to junk food.In short, do not deprive them completely of it as that will not help. | Children will find one way or the other to have it. | Make sure you give them junk food in limited quantities and at healthy periods of time."
    }
  ]
}
```

### Response
```json
{
  "extsumm": [
    {
      "text": "The Chrysler Building, the famous art deco New York skyscraper, will be sold for a small fraction of its previous sales price. | The deal, first reported by The Real Deal, was for $150 million, according to a source familiar with the deal. | Mubadala, an Abu Dhabi investment fund, purchased 90% of the building for $800 million in 2008. | Real estate firm Tishman Speyer had owned the other 10%. | The buyer is RFR Holding, a New York real estate company. | Officials with Tishman and RFR did not immediately respond to a request for comments. | It's unclear when the deal will close. | The building sold fairly quickly after being publicly placed on the market only two months ago. | The sale was handled by CBRE Group. | The incentive to sell the building at such a huge loss was due to the soaring rent the owners pay to Cooper Union, a New York college, for the land under the building. | The rent is rising from $7.75 million last year to $32.5 million this year to $41 million in 2028. | Meantime, rents in the building itself are not rising nearly that fast. | While the building is an iconic landmark in the New York skyline, it is competing against newer office towers with large floor-to-ceiling windows and all the modern amenities. | Still the building is among the best known in the city, even to people who have never been to New York. | It is famous for its triangle-shaped, vaulted windows worked into the stylized crown, along with its distinctive eagle gargoyles near the top. | It has been featured prominently in many films, including Men in Black 3, Spider-Man, Armageddon, Two Weeks Notice and Independence Day. | The previous sale took place just before the 2008 financial meltdown led to a plunge in real estate prices. | Still there have been a number of high profile skyscrapers purchased for top dollar in recent years, including the Waldorf Astoria hotel, which Chinese firm Anbang Insurance purchased in 2016 for nearly $2 billion, and the Willis Tower in Chicago, which was formerly known as Sears Tower, once the world's tallest. | Blackstone Group (BX) bought it for $1.3 billion 2015. | The Chrysler Building was the headquarters of the American automaker until 1953, but it was named for and owned by Chrysler chief Walter Chrysler, not the company itself. | Walter Chrysler had set out to build the tallest building in the world, a competition at that time with another Manhattan skyscraper under construction at 40 Wall Street at the south end of Manhattan. He kept secret the plans for the spire that would grace the top of the building, building it inside the structure and out of view of the public until 40 Wall Street was complete. | Once the competitor could rise no higher, the spire of the Chrysler building was raised into view, giving it the title.",
      "extractive_summary": [
        "The sale was handled by CBRE Group.",
        "Meantime, rents in the building itself are not rising nearly that fast.",
        "It is famous for its triangle-shaped, vaulted windows worked into the stylized crown, along with its distinctive eagle gargoyles near the top.",
        "Walter Chrysler had set out to build the tallest building in the world, a competition at that time with another Manhattan skyscraper under construction at 40 Wall Street at the south end of Manhattan. He kept secret the plans for the spire that would grace the top of the building, building it inside the structure and out of view of the public until 40 Wall Street was complete."
      ]
    },
    {
      "text": "Junk foods taste good that’s why it is mostly liked by everyone of any age group especially kids and school going children. | They generally ask for the junk food daily because they have been trend so by their parents from the childhood. | They never have been discussed by their parents about the harmful effects of junk foods over health. | According to the research by scientists, it has been found that junk foods have negative effects on the health in many ways. | They are generally fried food found in the market in the packets. | They become high in calories, high in cholesterol, low in healthy nutrients, high in sodium mineral, high in sugar, starch, unhealthy fat, lack of protein and lack of dietary fibers. | Processed and junk foods are the means of rapid and unhealthy weight gain and negatively impact the whole body throughout the life. | It makes able a person to gain excessive weight which is called as obesity. | Junk foods tastes good and looks good however do not fulfil the healthy calorie requirement of the body. | Some of the foods like french fries, fried foods, pizza, burgers, candy, soft drinks, baked goods, ice cream, cookies, etc are the example of high-sugar and high-fat containing foods. | It is found according to the Centres for Disease Control and Prevention that Kids and children eating junk food are more prone to the type-2 diabetes. | In type-2 diabetes our body become unable to regulate blood sugar level. | Risk of getting this disease is increasing as one become more obese or overweight. | It increases the risk of kidney failure. | Eating junk food daily lead us to the nutritional deficiencies in the body because it is lack of essential nutrients, vitamins, iron, minerals and dietary fibers. | It increases risk of cardiovascular diseases because it is rich in saturated fat, sodium and bad cholesterol. | High sodium and bad cholesterol diet increases blood pressure and overloads the heart functioning. | One who like junk food develop more risk to put on extra weight and become fatter and unhealthier. | Junk foods contain high level carbohydrate which spike blood sugar level and make person more lethargic, sleepy and less active and alert. | Reflexes and senses of the people eating this food become dull day by day thus they live more sedentary life. | Junk foods are the source of constipation and other disease like diabetes, heart ailments, clogged arteries, heart attack, strokes, etc because of being poor in nutrition. | Junk food is the easiest way to gain unhealthy weight. | The amount of fats and sugar in the food makes you gain weight rapidly. | However, this is not a healthy weight. | It is more of fats and cholesterol which will have a harmful impact on your health. | Junk food is also one of the main reasons for the increase in obesity nowadays.This food only looks and tastes good, other than that, it has no positive points. | The amount of calorie your body requires to stay fit is not fulfilled by this food. | For instance, foods like French fries, burgers, candy, and cookies, all have high amounts of sugar and fats. | Therefore, this can result in long-term illnesses like diabetes and high blood pressure. | This may also result in kidney failure. | Above all, you can get various nutritional deficiencies when you don’t consume the essential nutrients, vitamins, minerals and more. | You become prone to cardiovascular diseases due to the consumption of bad cholesterol and fat plus sodium. | In other words, all this interferes with the functioning of your heart. | Furthermore, junk food contains a higher level of carbohydrates. | It will instantly spike your blood sugar levels. | This will result in lethargy, inactiveness, and sleepiness. | A person reflex becomes dull overtime and they lead an inactive life. | To make things worse, junk food also clogs your arteries and increases the risk of a heart attack. | Therefore, it must be avoided at the first instance to save your life from becoming ruined.The main problem with junk food is that people don’t realize its ill effects now. | When the time comes, it is too late. | Most importantly, the issue is that it does not impact you instantly. | It works on your overtime; you will face the consequences sooner or later. | Thus, it is better to stop now.You can avoid junk food by encouraging your children from an early age to eat green vegetables. | Their taste buds must be developed as such that they find healthy food tasty. | Moreover, try to mix things up. | Do not serve the same green vegetable daily in the same style. | Incorporate different types of healthy food in their diet following different recipes. | This will help them to try foods at home rather than being attracted to junk food.In short, do not deprive them completely of it as that will not help. | Children will find one way or the other to have it. | Make sure you give them junk food in limited quantities and at healthy periods of time.",
      "extractive_summary": [
        "They generally ask for the junk food daily because they have been trend so by their parents from the childhood.",
        "It increases risk of cardiovascular diseases because it is rich in saturated fat, sodium and bad cholesterol.",
        "Reflexes and senses of the people eating this food become dull day by day thus they live more sedentary life.",
        "Junk foods are the source of constipation and other disease like diabetes, heart ailments, clogged arteries, heart attack, strokes, etc because of being poor in nutrition.",
        "The amount of calorie your body requires to stay fit is not fulfilled by this food.",
        "For instance, foods like French fries, burgers, candy, and cookies, all have high amounts of sugar and fats.",
        "Therefore, this can result in long-term illnesses like diabetes and high blood pressure.",
        "When the time comes, it is too late.",
        "Most importantly, the issue is that it does not impact you instantly.",
        "Children will find one way or the other to have it."
      ]
    }
  ]
}
```

### Component configuration
This is a component wrapped on the basis of [Bert Extractive Summarizer](https://github.com/dmmiller612/bert-extractive-summarizer).

| Parameter | Type | Default value | Description |
| --- | --- | --- | --- |
| ratio | float | 0.2 | Ratio of sentences to be kept in the extractive summary. |
| num_sentences | int | null | Number of sentences to be kept. Overrides ratio. |
| use_first | bool | false | Include the first sentence in the summary (helpful for news, stories, etc.). |
| algorithm | str | kmeans | Clustering algorithm to be used. (kmeans or gmm) |

Component's config can be modified in [`components/config.cfg`](components/config.cfg) for default values, or on the per API request basis at runtime:

```json
{
  "articles": [
    {
      "text": "The Chrysler Building, the famous art deco New York skyscraper, will be sold for a small fraction of its previous sales price. | The deal, first reported by The Real Deal, was for $150 million, according to a source familiar with the deal. | Mubadala, an Abu Dhabi investment fund, purchased 90% of the building for $800 million in 2008. | Real estate firm Tishman Speyer had owned the other 10%. | The buyer is RFR Holding, a New York real estate company. | Officials with Tishman and RFR did not immediately respond to a request for comments. | It's unclear when the deal will close. | The building sold fairly quickly after being publicly placed on the market only two months ago. | The sale was handled by CBRE Group. | The incentive to sell the building at such a huge loss was due to the soaring rent the owners pay to Cooper Union, a New York college, for the land under the building. | The rent is rising from $7.75 million last year to $32.5 million this year to $41 million in 2028. | Meantime, rents in the building itself are not rising nearly that fast. | While the building is an iconic landmark in the New York skyline, it is competing against newer office towers with large floor-to-ceiling windows and all the modern amenities. | Still the building is among the best known in the city, even to people who have never been to New York. | It is famous for its triangle-shaped, vaulted windows worked into the stylized crown, along with its distinctive eagle gargoyles near the top. | It has been featured prominently in many films, including Men in Black 3, Spider-Man, Armageddon, Two Weeks Notice and Independence Day. | The previous sale took place just before the 2008 financial meltdown led to a plunge in real estate prices. | Still there have been a number of high profile skyscrapers purchased for top dollar in recent years, including the Waldorf Astoria hotel, which Chinese firm Anbang Insurance purchased in 2016 for nearly $2 billion, and the Willis Tower in Chicago, which was formerly known as Sears Tower, once the world's tallest. | Blackstone Group (BX) bought it for $1.3 billion 2015. | The Chrysler Building was the headquarters of the American automaker until 1953, but it was named for and owned by Chrysler chief Walter Chrysler, not the company itself. | Walter Chrysler had set out to build the tallest building in the world, a competition at that time with another Manhattan skyscraper under construction at 40 Wall Street at the south end of Manhattan. He kept secret the plans for the spire that would grace the top of the building, building it inside the structure and out of view of the public until 40 Wall Street was complete. | Once the competitor could rise no higher, the spire of the Chrysler building was raised into view, giving it the title."
    }
  ],
  "component_cfg": {
    "extsumm": {"algorithm": "gmm", "use_first": true, "num_sentences": 3}
  }
}
```

```json
{
  "extsumm": [
    {
      "text": "The Chrysler Building, the famous art deco New York skyscraper, will be sold for a small fraction of its previous sales price. | The deal, first reported by The Real Deal, was for $150 million, according to a source familiar with the deal. | Mubadala, an Abu Dhabi investment fund, purchased 90% of the building for $800 million in 2008. | Real estate firm Tishman Speyer had owned the other 10%. | The buyer is RFR Holding, a New York real estate company. | Officials with Tishman and RFR did not immediately respond to a request for comments. | It's unclear when the deal will close. | The building sold fairly quickly after being publicly placed on the market only two months ago. | The sale was handled by CBRE Group. | The incentive to sell the building at such a huge loss was due to the soaring rent the owners pay to Cooper Union, a New York college, for the land under the building. | The rent is rising from $7.75 million last year to $32.5 million this year to $41 million in 2028. | Meantime, rents in the building itself are not rising nearly that fast. | While the building is an iconic landmark in the New York skyline, it is competing against newer office towers with large floor-to-ceiling windows and all the modern amenities. | Still the building is among the best known in the city, even to people who have never been to New York. | It is famous for its triangle-shaped, vaulted windows worked into the stylized crown, along with its distinctive eagle gargoyles near the top. | It has been featured prominently in many films, including Men in Black 3, Spider-Man, Armageddon, Two Weeks Notice and Independence Day. | The previous sale took place just before the 2008 financial meltdown led to a plunge in real estate prices. | Still there have been a number of high profile skyscrapers purchased for top dollar in recent years, including the Waldorf Astoria hotel, which Chinese firm Anbang Insurance purchased in 2016 for nearly $2 billion, and the Willis Tower in Chicago, which was formerly known as Sears Tower, once the world's tallest. | Blackstone Group (BX) bought it for $1.3 billion 2015. | The Chrysler Building was the headquarters of the American automaker until 1953, but it was named for and owned by Chrysler chief Walter Chrysler, not the company itself. | Walter Chrysler had set out to build the tallest building in the world, a competition at that time with another Manhattan skyscraper under construction at 40 Wall Street at the south end of Manhattan. He kept secret the plans for the spire that would grace the top of the building, building it inside the structure and out of view of the public until 40 Wall Street was complete. | Once the competitor could rise no higher, the spire of the Chrysler building was raised into view, giving it the title.",
      "extractive_summary": [
        "The Chrysler Building, the famous art deco New York skyscraper, will be sold for a small fraction of its previous sales price.",
        "The building sold fairly quickly after being publicly placed on the market only two months ago.",
        "Walter Chrysler had set out to build the tallest building in the world, a competition at that time with another Manhattan skyscraper under construction at 40 Wall Street at the south end of Manhattan. He kept secret the plans for the spire that would grace the top of the building, building it inside the structure and out of view of the public until 40 Wall Street was complete."
      ]
    }
  ]
}
```

### Implementation details
This repository only intergrates the [Bert Extractive Summarizer](https://github.com/dmmiller612/bert-extractive-summarizer) with [Sentence Transformers](https://www.sbert.net/) embeddings, the usage of general Hugging Face transformers, Elbow calculation, and coreference techniques are not implemented.


## Testing Celery mode locally
1 Install Redis on your local machine, and run it with:
```bash
redis-server --protected-mode no --bind 0.0.0.0 --loglevel debug
```

2 Make sure in your `.env`, these two variables are set correctly as `SERVICE_MODE=task` and `SERVICES_BROKER=redis://172.17.0.1:6379`

Then start your docker container with either `docker run` or `docker-compose up` as shown in the previous section.

3 On your local computer, run this python script: 
```python
from celery import Celery
celery = Celery(broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')
r = celery.send_task(
    'extsumm_task', 
    (
        'en', 
        [
            "The Chrysler Building, the famous art deco New York skyscraper, will be sold for a small fraction of its previous sales price. | The deal, first reported by The Real Deal, was for $150 million, according to a source familiar with the deal. | Mubadala, an Abu Dhabi investment fund, purchased 90% of the building for $800 million in 2008. | Real estate firm Tishman Speyer had owned the other 10%. | The buyer is RFR Holding, a New York real estate company. | Officials with Tishman and RFR did not immediately respond to a request for comments. | It's unclear when the deal will close. | The building sold fairly quickly after being publicly placed on the market only two months ago. | The sale was handled by CBRE Group. | The incentive to sell the building at such a huge loss was due to the soaring rent the owners pay to Cooper Union, a New York college, for the land under the building. | The rent is rising from $7.75 million last year to $32.5 million this year to $41 million in 2028. | Meantime, rents in the building itself are not rising nearly that fast. | While the building is an iconic landmark in the New York skyline, it is competing against newer office towers with large floor-to-ceiling windows and all the modern amenities. | Still the building is among the best known in the city, even to people who have never been to New York. | It is famous for its triangle-shaped, vaulted windows worked into the stylized crown, along with its distinctive eagle gargoyles near the top. | It has been featured prominently in many films, including Men in Black 3, Spider-Man, Armageddon, Two Weeks Notice and Independence Day. | The previous sale took place just before the 2008 financial meltdown led to a plunge in real estate prices. | Still there have been a number of high profile skyscrapers purchased for top dollar in recent years, including the Waldorf Astoria hotel, which Chinese firm Anbang Insurance purchased in 2016 for nearly $2 billion, and the Willis Tower in Chicago, which was formerly known as Sears Tower, once the world's tallest. | Blackstone Group (BX) bought it for $1.3 billion 2015. | The Chrysler Building was the headquarters of the American automaker until 1953, but it was named for and owned by Chrysler chief Walter Chrysler, not the company itself. | Walter Chrysler had set out to build the tallest building in the world, a competition at that time with another Manhattan skyscraper under construction at 40 Wall Street at the south end of Manhattan. He kept secret the plans for the spire that would grace the top of the building, building it inside the structure and out of view of the public until 40 Wall Street was complete. | Once the competitor could rise no higher, the spire of the Chrysler building was raised into view, giving it the title."
        ],
        {"extsumm": {"num_sentences": 3}}
    ),
    queue='extsumm')
r.get()
```