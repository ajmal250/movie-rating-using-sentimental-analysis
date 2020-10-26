from textblob import TextBlob
#string = ''
#for word in sys.argv[1:]:
#    string += word + ' '
#print(string)
string='very good'
print(string)
analysis = TextBlob(string).sentiment.polarity
print(analysis)