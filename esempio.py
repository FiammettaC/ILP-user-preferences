import clingo
import pandas as pd

class QuestionExample():
	topic: str
	num: int

	def to_asp_facts(self, file): #self
		#prg.append("question_type(topic(6), {}).".format(self.topic))
		#df = self.load_df(self, file)
		df = pd.read_excel(file)
		topics = ['management', 'qa', 'review', 'training', 'production', 'qc', 'logistics', 'maintenance']
		prg = []
		for idx in range(len(df)):
			prg.append("question_type(topic(" + str(idx) + "), " + df.topic.iloc[idx] + ").")
			prg.append("number_questions(topic(" + str(idx) + "), " + str(df.question.iloc[idx]) + ").")
			prg.append("detail_preference(topic(" + str(idx) + "), " + str(df.detail_preference.iloc[idx]) + ").")
			prg.append(" ")
		if (len(df.topic.unique())) == 8:
			prg.append(" ")
		else:
			missing = list(set(topics) - set(df.topic.unique()))
			for idx_, miss in enumerate(missing):
				prg.append("question_type(topic(" + str(idx+(idx_+1)) + "), " + miss + ").")
				prg.append("number_questions(topic(" + str(idx+(idx_+1)) + "), " + str(0) + ").")
				prg.append("detail_preference(topic(" + str(idx+(idx_+1)) + "), " + str(0) + ").")
				prg.append("")
		return "\n".join(prg)

if __name__ == '__main__':
	#prgs = ["a :- b. b. :~ a. [5@1]", "c :- b. b. :~ c. [3@1]"] # lista di QuestionExample
	prgs = ["data/df3.xlsx", "data/df7.xlsx", "data/df9.xlsx", "data/df18.xlsx", "data/df22.xlsx"]
	costs = []

	class ExampleCost():
		def __init__(self):
			self.cost = None
		def __call__(self,model):
			self.cost = model.cost
			return False

	for prg in prgs:
		prog = QuestionExample().to_asp_facts(prg)
		ctl = clingo.Control()
		ctl.add("base", [], prog)
		#ctl.add("base", [], prg.to_asp_facts())
		ctl.load("test_program.sp")
		ctl.ground([("base",[])])

		example_cost = ExampleCost()
		ctl.solve(on_model=example_cost)

		print("Cost for example", prg, "is", example_cost.cost)
