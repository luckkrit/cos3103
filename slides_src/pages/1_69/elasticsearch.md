---
layout: section
transition: fade
---

# Elasticsearch

---

## How Elasticsearch works?

- Elasticsearch shows the results by ranking with `_score` not just `match/unmatch`
- Elasticsearch uses the `BM25` algorithm, which is an improved version of `TF-IDF`
- This concept is a part of Information Retrieval (IR)

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

---

## Example

| Doc | เนื้อหา                            | จำนวนคำ (dl) |
| --- | -------------------------------- | ----- |
| 1   | elasticsearch is a search engine | 5     |
| 2   | search search search is fun      | 5     |
| 3   | kibana shows data in charts      | 5     |
| 4   | learn python for data science    | 5     |

> พยายามยกตัวอย่างคำไม่ยาวมากในแต่ละเอกสารเพราะว่า Elasticsearch จะมีกระบวนการบีบอัด ทำให้ค่าจริงอาจจะคลาดเคลื่อนจากความเป็นจริง

---
layout: two-cols-title
---

::title::
[Inverted Index Table]{class="text-2xl"}
- Elasticsearch (และ search engine ทุกตัว) ไม่ได้วิ่งไล่อ่านทุกเอกสารตอนค้นหา แต่สร้าง inverted index: ตารางที่ map จาก "คำ" ไปหา "เอกสารที่มีคำนั้น" ไว้ล่วงหน้า

::left::

| คำ (term)      | doc frequency (n) | postings (doc_id : tf) |
| ------------- | ----------------- | ---------------------- |
| a             | 1                 | 1:1                    |
| charts        | 1                 | 3:1                    |
| data          | 2                 | 3:1, 4:1               |
| elasticsearch | 1                 | 1:1                    |
| engine        | 1                 | 1:1                    |

::right::

| คำ (term)      | doc frequency (n) | postings (doc_id : tf) |
| ------------- | ----------------- | ---------------------- |
| for           | 1                 | 4:1                    |
| fun           | 1                 | 2:1                    |
| in            | 1                 | 3:1                    |
| is            | 2                 | 1:1, 2:1               |
| kibana        | 1                 | 3:1                    |

::default::

---
layout: two-cols-title
---

::title::
[Inverted Index Table]{class="text-2xl"}

::left::

| คำ (term)      | doc frequency (n) | postings (doc_id : tf) |
| ------------- | ----------------- | ---------------------- |
| learn         | 1                 | 4:1                    |
| python        | 1                 | 4:1                    |
| science       | 1                 | 4:1                    |
| **search**        | **2**                 | **1:1, 2:3**               |
| shows         | 1                 | 3:1                    |

::right::

- ค้นคำว่า `search` แล้ว engine แค่ lookup แถวนี้แถวเดียว ก็ได้ทั้ง:

- `n = 2` (ความยาวของ postings list = จำนวนเอกสารที่มีคำนี้) — ใช้คำนวณ idf โดยตรง
tf ของแต่ละเอกสาร (1 สำหรับ Doc 1, 3 สำหรับ Doc 2) — ไม่ต้องไล่อ่านเอกสารใหม่เลย

- นี่คือเหตุผลที่ค้นหาเร็ว: ต้นทุนไม่ขึ้นกับจำนวนเอกสารทั้งหมด (N) แต่ขึ้นกับความยาวของ postings list ของคำที่ค้นเท่านั้น

::default::

---

## How to evaluate TF-IDF of `search`

$$
N=4,\quad n=2
$$

$$
\operatorname{idf}(t)
=\ln\left(\frac{4}{2}\right)
=\ln(2)
\approx 0.6931
$$

| Doc | tf  | tf × idf            |
| --- | --- | ------------------- |
| 1   | 1   | 1 × 0.6931 = 0.6931 |
| 2   | 3   | 3 × 0.6931 = 2.0794 |
| 3   | 0   | 0                   |
| 4   | 0   | 0                   |

> สังเกต: Doc 2 คะแนนสูงกว่า Doc 1 พอดี 3 เท่า เพราะ TF-IDF ใช้ tf แบบเชิงเส้น (linear) ตรง ๆ

---

## Disadvantage of TF-IDF

1. ไม่มีเพดาน (no saturation): คำซ้ำ 100 ครั้ง คะแนนสูงกว่าซ้ำ 10 ครั้งถึง 10 เท่า ทั้งที่ไม่ได้เกี่ยวข้องมากขนาดนั้นจริง ๆ
2. ไม่ปรับตามความยาวเอกสาร (no length normalization): เอกสารยาว มีโอกาสมีคำซ้ำเยอะกว่าเอกสารสั้นอยู่แล้วโดยธรรมชาติ แต่ TF-IDF ไม่ได้หักลบส่วนนี้ออก

> นี่คือเหตุผลที่งานวิจัย IR พัฒนาต่อมาเป็น `BM25` (Best Matching 25)


---
layout: section
---

# BM25

---

## BM25 add $tf$ saturation ($k1$) and length normalization ($b$)


$$
\operatorname{score}(t,d)
=
\operatorname{idf}(t)
\times
\frac{
\operatorname{tf}(t,d)
}{
\operatorname{tf}(t,d)
+
k_1\left(1-b+b\frac{dl}{\operatorname{avgdl}}\right)
}
\times(k_1+1)
$$

$$
\operatorname{idf}(t)
=
\ln\left(
1+\frac{N-n+0.5}{n+0.5}
\right)
$$

> ($k_1$+1) เป็นค่าคงที่ สามารถคิดทีหลังได้

- $dl$ = ความยาวเอกสารนี้ (จำนวนคำ)
- $avgdl$ = ความยาวเฉลี่ยของเอกสารทั้งหมด
- $k1$ (ค่า default = 1.2) คุมว่า tf จะ "อิ่มตัว" (saturate) เร็วแค่ไหน
- $b$ (ค่า default = 0.75) คุมว่าจะหักลบตามความยาวเอกสารมากแค่ไหน (0 = ไม่หักเลย, 1 = หักเต็มที่)

---

## What is average document length?


| Doc | เนื้อหา                            | จำนวนคำ (dl) |
| --- | -------------------------------- | ----- |
| 1   | elasticsearch is a search engine | 5     |
| 2   | search search search is fun      | 5     |
| 3   | kibana shows data in charts      | 5     |
| 4   | learn python for data science    | 5     |

`avgdl` = **average document length** ความยาวเฉลี่ยของเอกสารทั้งหมดใน index (นับเป็นจำนวนคำ/token)

$$
\operatorname{avgdl}
=
\frac{dl_1 + dl_2 + \cdots + dl_N}{N}
$$

`avgdl = (5 + 5 + 5 + 5) / 4 = 5`

- ทุกเอกสารยาว 5 คำเท่ากัน → `avgdl = 5`

---

## Evaluate IDF

$$
\begin{aligned}
N &= 4, \quad n = 2, \quad \operatorname{avgdl} = 5 \\
k_1 &= 1.2, \quad b = 0.75
\end{aligned}
$$

$$
\begin{aligned}
\operatorname{idf}(t)
&= \ln\left(1+\frac{4-2+0.5}{2+0.5}\right) \\
&= \ln(1+1) \\
&= \ln(2) \\
&\approx 0.6931
\end{aligned}
$$


---

## Evaluate with BM25 of Doc 1

$$
\begin{aligned}
\operatorname{idf}(t) &= 0.6931 \\
\operatorname{tf}(t,d_1) &= 1 \\
dl &= 5 \\
\operatorname{avgdl} &= 5 \\
k_1 &= 1.2,\quad b = 0.75
\end{aligned}
$$

แทนค่าในสูตร BM25 ที่เราจัดรูปไว้:

$$
\operatorname{score}(t,d_1)
=
0.6931
\times
\frac{1}{
1+1.2\left(1-0.75+0.75\times\frac{5}{5}\right)
}
\times(1.2+1)
$$

จะได้

$$
\begin{aligned}
\operatorname{score}(t,d_1)
&= 0.6931 \times \frac{1}{1+1.2(1)} \times 2.2 \\[6pt]
&= 0.6931 \times \frac{1}{2.2} \times 2.2 \\[6pt]
&= \boxed{0.6931}
\end{aligned}
$$

---

## Evaluate with BM25 of Doc 2

$$
\begin{aligned}
\operatorname{idf}(t) &= 0.6931 \\
\operatorname{tf}(t,d_1) &= 3 \\
dl &= 5 \\
\operatorname{avgdl} &= 5 \\
k_1 &= 1.2,\quad b = 0.75
\end{aligned}
$$

แทนค่าในสูตร BM25 ที่เราจัดรูปไว้:

$$
\operatorname{score}(t,d_1)
=
0.6931
\times
\frac{3}{
3+1.2\left(1-0.75+0.75\times\frac{5}{5}\right)
}
\times(1.2+1)
$$

จะได้

$$
\begin{aligned}
\operatorname{score}(t,d_1)
&= 0.6931 \times \frac{3}{3+1.2(1)} \times 2.2 \\[6pt]
&= 0.6931 \times \frac{3}{4.2} \times 2.2 \\[6pt]
&= \boxed{1.0892}
\end{aligned}
$$

---

## Summary

| Doc | tf  | TF-IDF | BM25   |
| --- | --- | ------ | ------ |
| 1   | 1   | 0.6931 | 0.6931 |
| 2   | 3   | 2.0794 | 1.0892 |

---

## Test with Elasticsearch

```http
# Delete Index
DELETE demo

# Set number of shard to 1
PUT demo
{ "settings": { "number_of_shards": 1 } }

# Add data to demo
POST demo/_bulk?refresh
{"index":{"_id":"1"}}
{"content":"elasticsearch is a search engine"}
{"index":{"_id":"2"}}
{"content":"search search search is fun"}
{"index":{"_id":"3"}}
{"content":"kibana shows data in charts"}
{"index":{"_id":"4"}}
{"content":"learn python for data science"}

```

---

## Let Elasticsearch explain

```http

# Explain
GET demo/_search
{
  "explain": true,
  "query": { "match": { "content": "search" } }
}
```

> Result เป็น JSON ยาวมาก ต้องไปดูจาก Elasticsearch

<script setup>
const downloadUrl =
  `${import.meta.env.BASE_URL}json/elastic-result.json`
</script>

<a :href="downloadUrl" download>
  Download JSON
</a>

---

## Result

| Parameter | Document 2 | Document 1 |
|---|---:|---:|
| Term frequency (freq) | 3 | 1 |
| Document length (dl) | 5 | 5 |
| Average length (avgdl) | 5 | 5 |
| IDF | 0.6931 | 0.6931 |
| TF component | 0.7143 | 0.4545 |
| Boost ($k_1+1$) | 2.2 | 2.2 |
| **BM25 score** | **1.0892** | **0.6931** |