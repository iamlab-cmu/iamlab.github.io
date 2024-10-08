import urllib.request as urllib2
from bs4 import BeautifulSoup
import yaml
import re

"""
- title: Learning Closed-loop Dough Manipulation using a Differentiable Reset Module
	date: 2022-07-01
	img: ../pics/iros2022_logo.png
	arxiv_url: https://arxiv.org/abs/2207.04638
	pdf: https://arxiv.org/pdf/2207.04638.pdf
	site: https://sites.google.com/view/dough-manipulation/home
	code:
	authors: Carl Qi, Xingyu Lin, David Held
	venue: Robotics and Automation Letters (RA-L) with presentation at the International Conference on Intelligent Robots and Systems (IROS), 2022
	short_id: qi2022dough
	bibtex: "@ARTICLE{9830873,\n
	author={Qi, Carl and Lin, Xingyu and Held, David},\n
	journal={IEEE Robotics and Automation Letters},\n
	title={Learning Closed-Loop Dough Manipulation Using a Differentiable Reset Module},\n
	year={2022},\n
	volume={7},\n
	number={4},\n
	pages={9857-9864},\n
	doi={10.1109/LRA.2022.3191239}}"
	abstract:
		'Deformable object manipulation has many applications such as cooking and laundry folding in our daily lives. Manipulating elastoplastic objects such as dough is particularly challenging because dough lacks a compact state representation and requires contact-rich interactions. We consider the task of flattening a piece of dough into a specific shape from RGB-D images. While the task is seemingly intuitive for humans, there exist local optima for common approaches such as naive trajectory optimization. We propose a novel trajectory optimizer that optimizes through a differentiable "reset" module, transforming a single-stage, fixed-initialization trajectory into a multistage, multi-initialization trajectory where all stages are optimized jointly. We then train a closed-loop policy on the demonstrations generated by our trajectory optimizer. Our policy receives partial point clouds as input, allowing ease of transfer from simulation to the real world. We show that our policy can perform real-world dough manipulation, flattening a ball of dough into a target shape.'
	video_embed:
		<iframe width="560" height="315" src="https://www.youtube.com/embed/b1qKmgmei2U" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
"""

url = 'https://r-pad.github.io/publications/'
data = urllib2.urlopen(url)

soup = BeautifulSoup(data.read(), 'html.parser')
trs = soup.select('table tr')

def select_or_null(selector):
		sel = tr.select(selector)
		return sel if sel != [] else None

def parse_pub(tr):
		"""
		tr: bs4 element
		output: data
		"""
		data = {}

		div_abs = tr.find('div', id=re.compile('^abs*'))
		data['short_id'] = div_abs.attrs['id'].replace('abs', '') if div_abs is not None else None
	
		data['title'] = str(tr.select('td')[1].contents[0])

		try:	
			data['authors'] = str(tr.find('div', {'class': 'pubauthor'}).contents[0].strip())
		except Exception as e:
			print(e) 
			data['authors'] = None

		data['img'] = str(tr.select('td img')[0]['src'])

		pre_bib = tr.select('td div blockquote pre')
		data['bib'] = str(pre_bib[0].contents[0]).strip() if pre_bib != [] else None

		# year = re.split('(?i)year\s*=\s*(?:{|\")', str(pre_bib[0]))[1].split('}')[0].split('"')[0] if pre_bib != [] else None
		# data['date'] = f"{year}-01-01" if year is not None else None
		# data['date'] = None

		quote_abs = div_abs.select('blockquote') if div_abs is not None else None
		data['abs'] = str(quote_abs[0].contents[0]).strip() if quote_abs is not None else None

		pubjournal = tr.select('td div.pubjournal')
		if pubjournal != []:
			venue = str(pubjournal[0].contents[0])
			venue = re.sub('\s*-\s*', '', venue).strip() # trim whitespace and dash
			data['venue'] = venue

			award = pubjournal[0].select('award')
			data['award'] = ''.join([str(x) for x in pubjournal[0].contents[1:]]).split('\n')[0] if award != [] else None

		from collections import defaultdict
		data['links'] = {}
		data['site'] = None

		# data['site'] = tr.select('td div a[text="[Project Page]"]')
		for link in tr.select('td div[style="font-size:small"] a'):
			if 'Project' in link.text:
				data['site'] = str(link.attrs['href'])
			# elif 'arXiv' in link.text:
				# data['links']['arxiv_url'] = str(link.attrs['href'])
			# elif 'PDF' in link.text:
				# data['links']['pdf'] = str(link.attrs['href'])
			if 'Bibtex' not in link.text \
				and 'Abstract' not in link.text \
				and 'Project' not in link.text: # all other links (eg Poster)
				data['links'][link.text] = str(link.attrs['href'])

		data['video_embed'] = None

		return data

pubs = []
for tr in trs:
		# debug
		# if 'Occlusion' not in tr.select('td')[1].contents[0].text:
			# continue

		if tr.select('li') != []:
			break

		data = parse_pub(tr)
		pubs.append(data)
		# break

with open('../_data/pubs_gen.yml', 'w') as f:
		yaml.dump(pubs, f)

# print(soup)