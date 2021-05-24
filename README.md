# NEpali_Custom_NER
<h2>Overview</h2>
This project was designed on the concept to guide Nepalese people to read Official Government in a much more efficient way by highlighting all the important entities such as Municipalities, Cities, Karyalaya, etc. present in the document.<br>
<h2>Framework/Technology used</h2>
•	Spacy<br>
•	Flask<br>
•	Beautifull Soup 4<br>
•	Nepali Roman<br>
•	Pandas<br>
•	Numpy<br>
<h2>Application Overview:</h2>

 ![image](https://user-images.githubusercontent.com/32815205/119255330-f4d81a80-bbda-11eb-8a91-28a9395dd53c.png)

<h2>Instruction </h2>
<h4>Installing Packages</h4>

```python
pip install requirements.txt
```

<h4>Output Model(Source) </h4>
https://drive.google.com/drive/folders/1Mmzn3DoYILzUOYiF6ViXF7gndW16wa-1?usp=sharing
<h4>Load Output Model</h4>

```
nlp = spacy.load(R".\output\model-best")
```

<h4>Filter and Romanize Nepali text</h4>

```
new_inp='कपिलवस्तु नगरपालिका-३ सडवास्थित सडकमा अपरिचित व्यक्तिहरुको गोली प्रहारबाट कपिलवस्तु नगरपालिका-१ बस्ने ३४ वर्षीय दिपक पाण्डे र भारत सिदार्थनगर ग्राम चेतरी बजार बस्ने २६ वर्षीय ईयाज अख्तर मुसलमान बुधबार राति घाइते भएका छन् । लु.९ प ८५२१ नम्बरको मोटरसाइकलमा जर्लैया खोलाबाट तौलिहवातर्फ आउँदै गरेका उनीहरुलाई हाल नम्बर नखुलेको मोटरसाइकलमा आएका ३ जना अपरिचित व्यक्तिहरुले गोली प्रहार गर्दा घाइते भएको भन्ने खबर प्राप्त हुनासाथ जिल्ला प्रहरी कार्यालयबाट खटिएको प्रहरीले घाइते ईयाजलाई उपचारका लागि लागि जिल्ला अस्पताल तौलिहवा र दिपकलाई भैरहवा मेडिकल कलेज पठाएको छ । घटनास्थलबाट १ थान खोका, १ राउण्ड लाईभ बुलेट र १ थान चप्पल प्रहरीले बरामद गरेको छ । उक्त घटनामा संलग्न रहेको अभियोगमा कपिलवस्तु नगरपालिका-१ नयाँ टोल बस्ने १९ वर्षीय राजेश नाउ सहित ७ जनालाई प्रहरीले नियन्त्रणमा लिएर यस सम्बन्धमा थप अनुसन्धान गरिरहेको छ ।'
eng_to_nep = nepali_word_filter(new_inp)
```

<h4>Predicting Entities</h4>

```
doc = nlp1 (eng_to_nep)
spacy.displacy.render(doc, style="ent", jupyter=True)
```

