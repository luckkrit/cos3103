---
layout: section
transition: fade
---

# Elasticsearch

---

## How Elasticsearch works?

- Elasticsearch shows the results by ranking with `_score` not just `match/unmatch`
- Elasticsearch uses algorithm `BM25` based on `TF-IDF`

---
layout: section
---

## TF-IDF

---

## What is Term Frequency (TF)


<div class="border border-blue-400 rounded-xl p-2">

$$
TF(t,d) = \text{count}(t,d)
$$

$TF$ = จำนวนครั้งที่คำ $t$ ปรากฏในเอกสาร $d$

</div>

- ตัวอย่าง: ค้นคำว่า `search`

| เอกสาร | เนื้อหา                            | tf ของ "search" |
| ------ | -------------------------------- | --------------- |
| Doc 1  | elasticsearch is a search engine | 1               |
| Doc 2  | search search search is fun      | 3               |

---

## What is Inverse Document Frequency (IDF)


<div class="border border-blue-400 rounded-xl p-2">

$$
\operatorname{IDF}(t) = \ln\left(\frac{N}{n_t}\right)
$$

- $N$ = จำนวนเอกสารทั้งหมด
- $n$ = จำนวนเอกสารที่มีคำ $t$ อยู่
- $ln$ = Natural logarithm (ฐาน e)
</div>

ตัวอย่าง: 

- คำว่า "is" ปรากฏในแทบทุกเอกสาร → n มาก (🠩) → idf ต่ำ (🠫) (ไม่มีประโยชน์ในการแยกแยะ) 
- คำว่า "engine" ปรากฏน้อยเอกสาร → n น้อย (🠫) → idf สูง (🠩) (ช่วยแยกแยะได้ดี)

---

## What is TF-IDF?

<div class="border border-blue-400 rounded-xl p-2">

$$
\begin{aligned}
\operatorname{TF\text{-}IDF}(t,d) &= \operatorname{TF}(t,d)\times \operatorname{IDF}(t) \\
&= \operatorname{TF}(t,d)\times \ln\left(\frac{N}{n}\right)
\end{aligned}
$$

- $TF$ **สูง** → คำนี้ปรากฏบ่อยในเอกสารนั้น
- $IDF$ **สูง** → คำนี้ปรากฏในเอกสารจำนวนน้อยของคลังเอกสาร
- $TF × IDF$ → คำที่พบมากในเอกสารหนึ่ง แต่พบในเอกสารอื่นน้อย จะมีน้ำหนักสูง

</div>

- $TF-IDF$ ช่วยวัดความสำคัญของคำต่อเอกสาร โดยพิจารณาทั้งความถี่ภายในเอกสาร และความหายากในคลังเอกสาร


- $TF-IDF$ เป็นหนึ่งในแนวคิดพื้นฐานสำคัญของ Information Retrieval และการจัดอันดับเอกสาร ก่อนเรียนรู้ BM25