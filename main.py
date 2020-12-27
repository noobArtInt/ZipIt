from flask import Flask
from newspaper import Article as Blog
from googlesearch import search
import json, nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

app = Flask(__name__)


@app.route('/<query>')
def home(query):

	html = 'Searching for "{}", Please wait......<br>'.format(query)
	res = [i for i in search(query+' news',num_results = 10)]
	bunch =[]
	positivity= 0
	for i in res:
		try:
			blog = Blog(i)
			blog.download()
			blog.parse()
			pol = sid.polarity_scores(blog)
			html+= str(blog)+ '<br>'
			if pol['neu'] > 0.6 :
				html+= str(pol)+'<br>'
				if pol['neg'] != 0 or pol['pos'] != 0:
					
					if pol['neg'] > pol['pos']:
						positivity-=pol['neg']
						html+=(str(positivity)+'<br>')
					else:
						positivity+=pol['pos']
						html+=(str(positivity)+'<br>')

				bunch.append((blog.text, i))
		except:
			pass
		
		
	#sent+=(TextBlob(i).sentiment)

	return html+json.dumps(positivity)

if __name__ == '__main__':
   app.debug = True  #Set False for production
   app.run()
