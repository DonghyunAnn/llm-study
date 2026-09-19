# micrograd: 역전파를 100줄로

- 강의: Andrej Karpathy, [The spelled-out intro to neural networks and backpropagation: building micrograd](https://www.youtube.com/watch?v=VMj-3S1tku0) (2022-08, 2h25m). Zero to Hero 시리즈 1편.
- 코드: [karpathy/micrograd](https://github.com/karpathy/micrograd) (MIT, 커밋 `7bc720e` 2026-08-02 기준; `engine.py` 94줄, `nn.py` 60줄). 강의에서 실제로 타이핑한 노트북은 [nn-zero-to-hero/lectures/micrograd](https://github.com/karpathy/nn-zero-to-hero/tree/master/lectures/micrograd) (커밋 `73c3fcc`)에 있고, 저장소 코드와 조금 다르다(@sec-diff 참조).
- 정리 방식: 강의 노트북 두 개와 저장소 코드를 줄 단위로 분해했고, 핵심 수치 예제, 학습 루프, 저장소 테스트, moons 데모는 이 서버에서 실행해 출력을 기록했다(Python 3.9, torch 2.0.0, sklearn 0.24). graphviz 시각화만 실행하지 않았다(이 서버에 `dot`이 없다). 노트북 `cell` 번호는 0부터 세는 셀 인덱스이고, "전반"/"후반"은 `micrograd_lecture_first_half_roughly.ipynb` / `second_half`를 뜻한다. 강의 설명은 자동 생성 영어 자막(4,183줄)을 바탕으로 했고, 자막 오인식("10h" = tanh, "pi torch" = PyTorch, "jupiter" = Jupyter 등)은 문맥으로 교정했다. 화면(graphviz 그래프, 손그림, 위키백과 페이지)은 보지 못했다. 강의 노트북 파일명에 "roughly"가 붙어 있듯 영상에서 타이핑한 코드와 노트북이 완전히 같지는 않다.
- 검수: 초안을 Claude 서브에이전트와 Codex CLI가 독립적으로 자막·노트북·저장소 코드와 대조해 리뷰했고, 지적을 근거로 판정해 반영했다.
- 이 노트의 코드 블록에서 `# 각주:`로 시작하는 주석은 정리자가 단 것이고, 나머지 주석은 원본이다. 노트북 셀을 줄여 실은 블록은 그렇게 표시했다.

## 공식 자료 (영상 설명란)

- [micrograd 저장소](https://github.com/karpathy/micrograd) · [강의 노트북](https://github.com/karpathy/nn-zero-to-hero/tree/master/lectures/micrograd) · [연습문제 Colab](https://colab.research.google.com/drive/1FPTx1RXtBfc4MaTkf7viZZD4U2F9gtKN?usp=sharing)
- 공식 챕터 22개가 설명란에 있다. 아래 절의 시간은 그 챕터를 따른다.

## 한 줄 요약

카파시의 주장은 "micrograd가 신경망 학습에 필요한 전부이고, 나머지는 효율의 문제"라는 것이다. 신경망 학습의 전부는 "loss가 각 파라미터에 얼마나 민감한가(기울기)"를 구해서 파라미터를 그 반대 방향(loss가 줄어드는 방향)으로 조금씩 미는 것이다. micrograd는 그 기울기 계산(역전파)을 스칼라 하나짜리 `Value` 객체 100줄로 구현한다. PyTorch가 하는 일도 본질적으로 같고, 다른 점은 스칼라를 텐서(스칼라 배열)로 묶어 병렬로 계산한다는 것뿐이다. 스칼라 단위로 쪼개는 것은 실무에서는 과하지만 역전파를 이해하는 데는 그쪽이 낫다는 것이 카파시가 micrograd를 만든 이유다.

## 강의 구조와 코드 대응

| 시간 | 주제 | 코드 | minimind 대응 |
|---|---|---|---|
| 0:00–0:08 | micrograd 개요. 무엇을 만들 것인가 | README 예제 | — |
| 0:08–0:19 | 미분의 뜻. 수치 미분으로 감 잡기 | 전반 노트북 cell 1–6 | — |
| 0:19–0:32 | `Value` 객체와 그래프 시각화 | `engine.py` `__init__`, `__add__`, `__mul__`; `trace_graph.ipynb` | — |
| 0:32–0:53 | 수동 역전파 ① 단순 식, 한 스텝 최적화 미리보기 | 전반 노트북 cell 9–11 (`lol()` 수치 검증 포함) | — |
| 0:53–1:09 | 수동 역전파 ② 뉴런 하나 (tanh) | 전반 노트북 cell 13–30 | `model_minimind.py` `FeedForward`의 활성 함수 |
| 1:09–1:22 | 연산마다 `_backward` 구현, 위상 정렬로 전체 그래프 역전파 | `engine.py` `_backward` 클로저, `backward()` | `loss.backward()` |
| 1:22–1:27 | 버그: 같은 노드를 두 번 쓰면 기울기가 덮어써짐 → `+=` | `engine.py` 18–19, 29–30 | — |
| 1:27–1:39 | tanh를 exp로 분해, 나머지 연산 추가 | `engine.py` `__pow__`, `__truediv__`, `__neg__`, r-연산 | — |
| 1:39–1:44 | PyTorch로 같은 계산 | 후반 노트북 cell 12–13 (저장소 `test/test_engine.py`는 2:18 워크스루에서) | minimind 전체가 이 위에서 돈다 |
| 1:44–1:51 | Neuron → Layer → MLP | `nn.py` | `FeedForward`, `MiniMindBlock` |
| 1:51–2:14 | 데이터셋, loss, 파라미터 수집, 경사하강 학습 루프 | 후반 노트북 cell 15–18; `demo.ipynb` | `train_pretrain.py`의 학습 루프 |
| 2:14–2:25 | 요약, 저장소 코드 워크스루, PyTorch 내부의 tanh backward | 저장소 전체 | — |

---

## micrograd 개요 (0:00–0:08) {#sec-overview}

카파시는 2년 전 소스만 올려 둔 micrograd를 이번에 처음부터 다시 만들어 보이겠다고 시작한다. micrograd는 autograd(automatic gradient) 엔진이다. 역전파, 즉 "loss의 가중치에 대한 기울기를 효율적으로 구하는 알고리즘"을 구현하고, 그것으로 가중치를 반복해서 조정해 loss를 줄인다. PyTorch나 JAX 같은 현대 라이브러리의 수학적 핵심이 이것이다.

README 예제(`a=-4, b=2`로 `g`를 만들고 `g.backward()`)를 보여주며 두 가지를 짚는다. 이 식은 "지원하는 연산을 자랑하려고 지어낸 무의미한 식"이고, 신경망도 결국 이런 수식의 한 종류(입력 데이터와 가중치를 받아 예측이나 loss를 내는 식)라는 것. 역전파는 신경망과 무관하게 임의의 수식에 적용되고, 우리가 그것을 신경망 학습에 쓸 뿐이다. 코드는 `engine.py` 약 100줄과 `nn.py` 약 50줄, 합쳐 150줄이며 "이게 신경망 학습을 이해하는 데 필요한 전부이고 나머지는 효율"이라고 말한다.

## 미분이란 무엇인가 (0:08–0:19) {#sec-derivative}

강의는 미분의 정의 $\frac{df}{dx} = \lim_{h\to 0}\frac{f(x+h)-f(x)}{h}$를 "x를 아주 조금 밀었을 때 f가 얼마나, 어느 방향으로 반응하는가"로 읽는다. 공식이 아니라 이 감각이 역전파 전체의 기초다.

전반 노트북 cell 4의 실험(강의에서는 먼저 $x=3$, $h=0.001$로 한다). 실행 결과를 붙였다.

```python
def f(x):
  return 3*x**2 - 4*x + 5

h = 0.000001
x = 2/3
(f(x + h) - f(x))/h        # 각주: 수치 미분. 해석적으로는 6x-4 이고 x=2/3에서 0
```

출력: `2.999e-06`. 0에 매우 가깝다. $x = 2/3$은 이 포물선의 최저점이라 어느 쪽으로 밀어도 f가 거의 변하지 않는다. 강의에서는 먼저 $x=3$에서 기울기 14($6x-4$), $x=-3$에서 $-22$를 같은 방법으로 확인하고, 두 가지를 덧붙인다. 신경망에서는 수만 항짜리 식을 기호적으로 미분하는 사람이 없으니 정의로 돌아가 "조금 밀었을 때의 반응"으로 이해하라는 것, 그리고 $h$를 너무 작게 잡으면 부동소수점 표현 한계 때문에 오히려 틀린 값이 나온다는 것.

입력이 여러 개일 때는 하나씩 민다.

```python
a, b, c = 2.0, -3.0, 10.0
d1 = a*b + c
c += 0.0001                # 각주: c만 조금 밀고
d2 = a*b + c
(d2 - d1)/0.0001           # 각주: d가 c에 얼마나 반응하나 = ∂d/∂c  (전반 노트북 cell 6을 줄인 것)
```

출력: `0.9999999999976694` (≈ 1). $d = ab + c$이므로 $\partial d/\partial c = 1$, $\partial d/\partial a = b = -3$, $\partial d/\partial b = a = 2$. 강의는 값을 보기 전에 부호를 먼저 추론하게 한다. $a$를 키우면 $b=-3$과 곱해지니 $d$는 줄어든다(실제로 4 → 3.9996), $b$를 키우면 $a=2$가 양수라 늘어난다. 수치 미분은 첫 수동 역전파 구간에서 각 기울기를 확인하는 도구로 다시 쓰인다.

---

## Value 객체: 계산 그래프 만들기 (0:19–0:32) {#sec-value}

핵심 아이디어는 **연산을 할 때 결과값만 남기지 않고, 그 결과가 어떤 입력에서 어떤 연산으로 나왔는지를 함께 기록**하는 것이다. 이렇게 하면 마지막 출력에서 거꾸로 따라 내려가며 기울기를 나눠줄 수 있다.

### `__init__`

```python
class Value:
    """ stores a single scalar value and its gradient """

    def __init__(self, data, _children=(), _op=''):
        self.data = data                 # 각주: 실제 값. 스칼라 하나
        self.grad = 0                    # 각주: dL/d(self). 역전파 전에는 0. "이 값이 최종 출력에 미치는 영향"
        # internal variables used for autograd graph construction
        self._backward = lambda: None    # 각주: 이 노드의 지역 미분 규칙. 잎 노드는 할 일이 없어서 빈 함수
        self._prev = set(_children)      # 각주: 이 값을 만든 입력 노드들(=자식). 그래프의 간선
        self._op = _op # the op that produced this node, for graphviz / debugging / etc
```

- **무엇**: 숫자 하나에 기울기 칸과 "자식 포인터"를 붙인 상자. 카파시와 코드(`_children`)는 출력 쪽에서 봐서 **입력 노드를 자식**이라 부른다. 이 노트도 그 용어를 따른다.
- **왜**: `_prev`가 있어야 출력에서 입력으로 거슬러 갈 수 있다. 강의는 이것을 "어떤 값이 어떤 값을 만들었는지 포인터를 유지하는 연결 조직"이라 부른다. `_op`는 계산에 쓰이지 않고 그래프를 그릴 때만 쓴다. 강의 노트북 버전에는 `label` 인자가 하나 더 있는데, 시각화에서 노드 이름을 붙이기 위한 것이다.
- `_children`을 튜플로 받아 `set`으로 바꾸는 이유를 카파시는 "원래 코드에서 그렇게 했고 아마 효율 때문이었을 것"이라고만 말한다. (내 해석: 순서가 필요 없으니 집합으로 충분하다.)
- `grad`를 0으로 초기화하는 뜻: "영향 없음". 역전파 전에는 모든 값이 출력에 영향을 주지 않는다고 가정하는 셈이다.

### `__add__`, `__mul__`

```python
    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)   # 각주: a + 1 처럼 숫자가 오면 Value로 감쌈
        out = Value(self.data + other.data, (self, other), '+')       # 각주: 값은 지금 계산(forward). 부모 둘과 연산 기호를 기록

        def _backward():
            self.grad += out.grad        # 각주: 덧셈의 지역 미분은 1. out의 기울기를 그대로 양쪽에 흘려보냄
            other.grad += out.grad
        out._backward = _backward        # 각주: 정의만 해 두고 호출은 backward()가 나중에 함

        return out

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')

        def _backward():
            self.grad += other.data * out.grad    # 각주: d(a*b)/da = b. 상대편 값을 곱해서 흘려보냄
            other.grad += self.data * out.grad    # 각주: d(a*b)/db = a
        out._backward = _backward

        return out
```

- **무엇**: 연산 하나 = forward 값 계산 + 그 연산의 미분 규칙을 담은 클로저.
- **왜 클로저인가**: `_backward`는 `self`, `other`, `out` 세 객체를 붙잡고 있어야 한다. 함수 안에 함수를 정의하면 그 변수들이 그대로 잡힌다. 강의의 요지는 각 노드가 "출력의 기울기를 입력의 기울기로 연쇄하는 작은 연쇄법칙 조각"을 스스로 갖고 있다는 것이다.
- **왜 `+=`인가**: 같은 `Value`가 식에 두 번 쓰이면 두 경로에서 오는 기울기를 더해야 한다. 이 이유는 [@sec-bug]에서 버그로 등장한다. 영상에서 처음 쓴 버전은 `self.grad = 1.0 * out.grad`처럼 대입이었다(공개된 노트북에는 이미 `+=`로 고쳐져 있다).
- 덧셈은 "기울기 분배기", 곱셈은 "기울기에 상대편 값을 곱하는 스위치"로 읽으면 된다.

### 그래프 그리기 (`trace_graph.ipynb`)

```python
def trace(root):
    nodes, edges = set(), set()
    def build(v):
        if v not in nodes:
            nodes.add(v)
            for child in v._prev:          # 각주: 자식(입력) 포인터를 따라 뿌리(출력)에서 잎(입력)으로 내려감
                edges.add((child, v))
                build(child)
    build(root)
    return nodes, edges
```

`draw_dot`은 각 노드를 `data | grad` 상자로, 연산은 작은 원으로 그린다. 연산 노드는 그래프에 실제로 있는 객체가 아니라 그림을 보기 좋게 하려고 `draw_dot`이 끼워 넣은 가짜 노드다. 강의 내내 이 그림 위에서 기울기를 손으로 채워 넣는다. 직접 실행하려면 `pip install graphviz`와 시스템 `dot`이 필요하다(이 서버에는 없어서 원본 그림은 재현하지 않았다). 아래는 같은 그래프를 다시 그린 것이다.

![[@sec-manual-1]의 예제 $L = (a\cdot b + c)\cdot f$의 계산 그래프. 각 상자의 `data`는 forward 값, `grad`는 `L.backward()` 뒤의 $\partial L/\partial(\cdot)$. 강의의 `draw_dot` 출력을 본떠 다시 그렸다(adapted from the lecture's graphviz view).](diagrams/computation-graph.png){#fig-graph}

---

## 수동 역전파 ① 단순 식 (0:32–0:53) {#sec-manual-1}

강의는 `backward()`를 만들기 전에 손으로 먼저 한다. 식은

$$e = a b,\quad d = e + c,\quad L = d f$$

값은 $a=2, b=-3, c=10, f=-2$. forward하면 $e=-6, d=4, L=-8$.

역전파는 출력 $L$에서 시작한다. $\partial L/\partial L = 1$. 그다음 한 단계씩 연쇄법칙을 적용한다.

| 노드 | 지역 미분 | 기울기 $\partial L/\partial(\cdot)$ |
|---|---|---|
| $L$ | — | 1 |
| $d$ | $\partial L/\partial d = f$ | $-2$ |
| $f$ | $\partial L/\partial f = d$ | $4$ |
| $e$ | $\partial d/\partial e = 1$ | $-2 \cdot 1 = -2$ |
| $c$ | $\partial d/\partial c = 1$ | $-2$ |
| $a$ | $\partial e/\partial a = b$ | $-2 \cdot (-3) = 6$ |
| $b$ | $\partial e/\partial b = a$ | $-2 \cdot 2 = -4$ |

저장소 코드로 확인한 출력: `L=-8.0 | grads a,b,c,f,e,d = 6.0 -4.0 -2.0 4.0 -2.0 -2.0`. 표와 같다.

카파시는 덧셈 노드 $d$를 지나 $\partial L/\partial c$를 구하는 이 단계를 "역전파의 핵심(crux), 이 노드의 기울기를 이해하면 역전파와 신경망 학습 전부를 이해한 것"이라고 말한다. 지역 미분 자체도 정의로 유도해 보인다. $\partial(df)/\partial d = \lim \frac{(d+h)f - df}{h} = f$, $\partial(c+e)/\partial c = \lim \frac{(c+h+e)-(c+e)}{h} = 1$. 덧셈 노드는 자기 지역 미분($\partial d/\partial c = 1$)만 알고 그래프의 나머지는 모른다. 그 지역 미분과 위에서 내려온 $\partial L/\partial d$를 **연쇄법칙**으로 곱한다. 위키백과의 비유를 그대로 옮기면, 자동차가 자전거보다 2배 빠르고 자전거가 걷는 사람보다 4배 빠르면 자동차는 걷는 사람보다 $2 \times 4 = 8$배 빠르다. $\partial L/\partial a = \partial L/\partial e \cdot \partial e/\partial a$. 덧셈은 지역 미분이 1이라 기울기를 "그냥 통과시키는 라우터"이고, 역전파 전체는 연쇄법칙을 그래프 뒤쪽으로 재귀적으로 적용하는 것이다.

강의는 매 단계를 수치 미분으로 검증한다("inline gradient check"). 예를 들어 $c$를 $h$만큼 밀어 $L$의 변화를 재면 $-2$가 나온다.

### 최적화 한 스텝 미리보기 (0:51)

```python
a.data += 0.01 * a.grad     # 각주: 기울기 방향으로 조금 밀면 L이 커진다 (여기서는 L을 키우는 방향). 강의에서 L은 -8 → -7
b.data += 0.01 * b.grad
c.data += 0.01 * c.grad
f.data += 0.01 * f.grad
# 각주: 전반 노트북 cell 10은 여기서 e, d, L을 다시 계산해 print한다. 출력 -7.286496 (L이 -8에서 커졌다)
```

학습에서는 loss를 줄여야 하므로 부호가 반대(`-=`)가 된다. 이 한 줄이 경사하강법의 전부다.

---

## 수동 역전파 ② 뉴런 하나 (0:53–1:09) {#sec-manual-2}

뉴런은 입력에 가중치(시냅스 강도)를 곱해 더하고 편향(이 뉴런이 얼마나 쉽게 발화하는지)을 더한 뒤 비선형 함수를 씌운 것이다. 강의는 tanh를 쓴다. 입력이 크면 1, 작으면 $-1$로 부드럽게 눌러 주는(squash) 함수다.

$$o = \tanh(x_1 w_1 + x_2 w_2 + b)$$

강의 노트북 값: $x_1=2, x_2=0, w_1=-3, w_2=1, b=6.8813735870195432$. $b$가 이상한 숫자인 이유를 카파시가 직접 말한다. $n = 0.8814$가 되어 $\tanh(n)=0.7071$, 즉 $1 - o^2 = 0.5$로 기울기가 "머릿속으로 따라갈 수 있는 깔끔한 숫자"가 되게 하려는 것이다. tanh를 원자 연산으로 쪼개지 않고 통째로 구현하는 이유도 설명한다. 연산의 추상화 수준은 자유이고, 그 연산의 지역 미분만 알면 된다.

tanh의 미분은 $1 - \tanh^2$ 이다. 강의 노트북에 추가된 메서드:

```python
  def tanh(self):
    x = self.data
    t = (math.exp(2*x) - 1)/(math.exp(2*x) + 1)   # 각주: tanh 정의. math.tanh를 안 쓰고 식을 드러냄
    out = Value(t, (self, ), 'tanh')              # 각주: 입력이 하나라 _children도 하나

    def _backward():
      self.grad += (1 - t**2) * out.grad          # 각주: d tanh/dn = 1 - tanh²  (t는 forward 때 계산한 값 재사용)
    out._backward = _backward

    return out
```

실행 결과 (`o.backward()` 후): `o=0.7071 | grads x1,w1,x2,w2,b,n = [-1.5, 1.0, 0.5, 0.0, 0.5, 0.5]`.

읽는 법: $\partial o/\partial n = 1 - \tanh^2(n) = 0.5$(tanh의 미분은 강의에서 위키백과를 찾아 가져온다). 덧셈 노드들은 0.5를 그대로 통과시켜 $b$, $x_1w_1$, $x_2w_2$의 기울기가 모두 0.5. 곱셈 노드에서 $x_1$의 기울기는 $0.5 \times w_1 = -1.5$, $w_1$의 기울기는 $0.5 \times x_1 = 1.0$. $w_2$의 기울기가 0인 이유는 $x_2 = 0$이라 $w_2$를 아무리 바꿔도 출력이 안 변하기 때문이다. 이것이 "기울기 = 민감도"의 뜻이다. 실제 신경망에서 관심 있는 것은 $w$들의 기울기다. 최적화에서 바꾸는 것이 가중치이기 때문이다.

---

## `_backward`와 위상 정렬 (1:09–1:27) {#sec-backward}

손으로 하던 것을 자동화한다. 각 노드의 `_backward`를 **올바른 순서로** 호출하기만 하면 된다. 순서가 중요한 이유: 어떤 노드의 `_backward`는 그 노드의 `grad`가 완성된 뒤에 호출되어야 한다. 그렇지 않으면 미완성 기울기를 부모에게 넘긴다.

```python
    def backward(self):

        # topological order all of the children in the graph
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:     # 각주: 자기 자식(입력)들을 먼저 전부 넣고
                    build_topo(child)
                topo.append(v)            # 각주: 그다음에 자기를 넣는다 → 입력이 항상 출력보다 앞에 온다
        build_topo(self)

        # go one variable at a time and apply the chain rule to get its gradient
        self.grad = 1                     # 각주: dL/dL = 1. 출발점
        for v in reversed(topo):          # 각주: 뒤집으면 출력 → 입력 순서. 각 노드가 받은 기울기를 부모에게 나눠줌
            v._backward()
```

- **무엇**: 깊이 우선 탐색으로 위상 정렬을 만들고, 거꾸로 돌며 각 노드의 미분 규칙을 실행한다. 강의는 이 단계를 셋으로 나눠 보여준다. 먼저 각 연산에 `_backward` 클로저를 달고, `o._backward()`, `n._backward()`, ... 를 손으로 올바른 순서로 호출해 같은 기울기가 나오는 것을 확인한 뒤, 그 순서를 위상 정렬로 자동화한다. 중간에 `out._backward = _backward()`처럼 함수를 저장하지 않고 호출해 버려서 `'NoneType' object is not callable`이 나는 실수도 그대로 보여준다.
- **왜 위상 정렬인가**: 어떤 노드의 `_backward`도 "그 뒤에 있는 것들이 전부 처리된 뒤"에 호출되어야 한다. 그래프는 DAG(방향 비순환 그래프)이고, 위상 정렬은 "모든 간선이 한 방향으로만 향하는" 배열이다. `build_topo`는 자식(입력)을 전부 넣은 다음에야 자기를 넣으므로 "내 자식이 모두 리스트에 있어야 내가 들어간다"는 불변식이 유지되고, 이걸 뒤집으면 어떤 노드든 자기 기울기를 다 받은 뒤에 `_backward`가 호출됨이 보장된다.
- (내 해석) `visited`가 없으면 같은 노드가 여러 번 들어가 `_backward`가 여러 번 불려 기울기가 중복 누적된다.
- 이 함수 하나가 PyTorch의 `loss.backward()`에 해당한다.

### 버그: 같은 노드를 두 번 쓰면 (1:22–1:27) {#sec-bug}

강의 초반 버전은 `_backward` 안에서 `self.grad = ...`(대입)였다. 그러면 이런 식에서 틀린다.

```python
a = Value(3.0)
b = a + a          # 각주: a가 두 경로로 b에 기여
b.backward()
a.grad             # 각주: 정답은 2 (db/da = 2). 대입이면 두 번째 경로가 첫 번째를 덮어써 1이 나온다. (전반 노트북 cell 31을 줄인 것)
```

실행 결과(저장소 코드, `+=` 버전): `a.grad = 2`. 대입이면 `self`와 `other`가 같은 객체라 1을 쓰고 다시 1을 덮어써 1이 남는다. 강의는 두 번째 예도 든다. `d = a*b`, `e = a+b`, `f = d*e`에서 `e._backward()`가 `a`, `b`에 기울기를 놓은 뒤 `d._backward()`가 그것을 덮어쓴다. 지금까지의 예에서 버그가 안 보인 이유는 모든 변수가 정확히 한 번씩만 쓰였기 때문이다. 미적분에서 여러 경로의 기여는 더해진다(다변수 연쇄법칙). 그래서 모든 `_backward`가 `+=`를 쓰고, `grad`가 0에서 시작하므로 누적이 올바르다.

강의 노트북에는 관련 메모가 하나 더 있다. `exp`의 `_backward`를 영상에서는 `=`로 잘못 썼고 노트북에서 `+=`로 고쳤다는 주석이 코드에 남아 있다.

---

## tanh 분해와 나머지 연산 (1:27–1:39) {#sec-more-ops}

강의는 tanh를 `exp`, 나눗셈, 뺄셈으로 풀어 써도 같은 기울기가 나온다는 것을 보인다. 요점은 **연산의 단위는 임의**라는 것이다. tanh를 통째로 하나의 노드로 봐도 되고, 그 안의 exp와 나눗셈까지 쪼개도 된다. 각 조각이 자기 지역 미분만 알면 연쇄법칙이 나머지를 해결한다.

$$\tanh(n) = \frac{e^{2n}-1}{e^{2n}+1}$$

```python
e = (2*n).exp()
o = (e - 1) / (e + 1)     # 각주: 이 두 줄이 __rmul__(2*n), __sub__/__neg__, 숫자를 Value로 감싸는 __add__, __truediv__/__pow__를 전부 요구한다
```

실행 결과: `exp-decomposed o=0.7071 x1.grad=-1.5 w1.grad=1.0`. tanh 노드 하나로 했을 때와 같다.

그래서 저장소 `engine.py`에는 아래 연산들이 있다. tanh는 저장소에는 없고 ReLU만 있다.

```python
    def __pow__(self, other):
        assert isinstance(other, (int, float)), "only supporting int/float powers for now"   # 각주: 지수는 상수만. Value**Value는 미지원
        out = Value(self.data**other, (self,), f'**{other}')

        def _backward():
            self.grad += (other * self.data**(other-1)) * out.grad   # 각주: d(x^k)/dx = k·x^(k-1)
        out._backward = _backward

        return out

    def relu(self):
        out = Value(0 if self.data < 0 else self.data, (self,), 'ReLU')

        def _backward():
            self.grad += (out.data > 0) * out.grad   # 각주: 양수였으면 그대로 통과(1), 음수였으면 차단(0). bool이 0/1로 곱해짐. 미분이 정의되지 않는 0에서는 이 구현이 0을 택함
        out._backward = _backward

        return out

    # 각주: 이 사이의 backward()는 위 절에 실었다
    def __neg__(self): # -self
        return self * -1                  # 각주: 새 미분 규칙을 안 만들고 곱셈으로 환원. 아래 전부 같은 전략

    def __radd__(self, other): # other + self
        return self + other               # 각주: 1 + a 처럼 왼쪽이 숫자일 때 파이썬이 이걸 부른다

    def __sub__(self, other): # self - other
        return self + (-other)

    def __rsub__(self, other): # other - self
        return other + (-self)

    def __rmul__(self, other): # other * self
        return self * other

    def __truediv__(self, other): # self / other
        return self * other**-1           # 각주: a/b = a · b^(-1). 나눗셈의 미분 규칙도 따로 안 만든다

    def __rtruediv__(self, other): # other / self
        return other * self**-1
```

- **왜 이렇게 짰나**: 미분 규칙을 직접 가진 "원자" 연산은 저장소에서 `+`, `*`, `**`, `relu` 네 개, 강의 노트북에서는 `relu` 대신 `tanh`와 `exp`를 두어 다섯 개다. 나머지는 이들의 조합으로 환원해서 코드와 실수 가능성을 줄인다.
- `a + 1`이 처음에 실패하는 이유는 `other`가 `int`라 `.data`가 없기 때문이고, 그래서 `isinstance` 검사로 감싼다. `a * 2`는 되지만 `2 * a`는 `int`가 `Value`를 곱할 줄 몰라 실패한다. 파이썬은 왼쪽 피연산자가 처리를 거부하면 오른쪽의 `__rmul__`을 시도하고, 거기서 순서를 바꿔 `a * 2`로 돌린다. 카파시는 이것을 "불행하고 자명하지 않은 부분"이라 부른다.
- `exp`의 미분은 $e^x$ 자신이라 `out.data * out.grad`로 쓴다(이미 계산한 값을 재사용). `__pow__`는 멱법칙 $n x^{n-1}$이고, 지수를 `Value`로 허용하면 미분식이 달라지므로 상수로 제한한다.

README 예제로 이 연산들의 조합을 확인했다(`__rsub__`만은 이 예제에서 호출되지 않는다). 실행 결과: `g=24.7041`, `a.grad=138.8338`, `b.grad=645.5773`. README에 적힌 값과 같다.

---

## PyTorch로 같은 계산 (1:39–1:44) {#sec-pytorch}

저장소의 테스트는 micrograd와 PyTorch의 forward 값과 기울기가 같은지를 비교한다.

```python
def test_sanity_check():

    x = Value(-4.0)
    z = 2 * x + 2 + x
    q = z.relu() + z * x
    h = (z * z).relu()
    y = h + q + q * x
    y.backward()
    xmg, ymg = x, y                     # 각주: micrograd 쪽 결과를 보관

    x = torch.Tensor([-4.0]).double()   # 각주: float32로 만든 뒤 float64로 변환. micrograd(파이썬 float)와 맞추려는 것이지만 -4.0처럼 정확히 표현되는 값이 아니면 float32 반올림은 남는다
    x.requires_grad = True              # 각주: 잎 텐서는 기본적으로 기울기를 안 만든다(효율). 켜야 .grad가 생김
    z = 2 * x + 2 + x
    q = z.relu() + z * x
    h = (z * z).relu()
    y = h + q + q * x
    y.backward()                        # 각주: micrograd의 backward()와 같은 역할. 텐서 하나짜리라 스칼라와 동일
    xpt, ypt = x, y

    # forward pass went well
    assert ymg.data == ypt.data.item()
    # backward pass went well
    assert xmg.grad == xpt.grad.item()  # 각주: .item()으로 파이썬 숫자로 꺼냄
```

이 서버에서 `python -m pytest`: `2 passed in 1.28s`.

- 강의는 같은 tanh 뉴런을 PyTorch로 다시 만들어 forward 0.7071과 기울기 0.5, 0, $-1.5$, 1이 일치하는 것을 보인다. `.double()`은 파이썬 float(float64)과 정확히 맞추기 위한 것이고(PyTorch 기본은 float32), `requires_grad`가 기본 False인 이유는 입력 데이터 같은 잎 노드의 기울기는 보통 필요 없어서 효율을 위해서다.
- PyTorch의 텐서는 micrograd의 `Value`에 (1) 여러 숫자를 한 번에 담는 배열, (2) 그 배열 위에서 병렬로 도는 연산이 더해진 것이다(GPU 얘기는 강의 끝의 CUDA 커널에서만 나온다). `.data`, `.grad`, `.backward()`라는 API 이름까지 같고, PyTorch에는 기울기 추적 여부를 정하는 `requires_grad`가 추가로 있다. 강의 마지막(2:21)에는 PyTorch 소스에서 tanh의 backward를 찾는 장면이 있다. `tanh`를 검색하면 406개 파일에 2,800건이 나와 15분을 헤맸고, 결국 `BinaryOpsKernel`(tanh는 이항 연산이 아닌데도) 안의 CPU 커널에서 `a * (1 - b*b)` 꼴, CUDA 커널에서 한 줄짜리 같은 식을 찾는다. "이 라이브러리들은 쓰라고 만든 것이지 들여다보라고 만든 것이 아니다." 그리고 `torch.autograd.Function`을 상속해 forward와 backward만 정의하면 새 연산을 레고 블록처럼 등록할 수 있다는 예(LegendrePolynomial3)를 보여준다. micrograd의 `_backward` 클로저와 같은 계약이다.

---

## Neuron → Layer → MLP (1:44–1:51) {#sec-nn}

`nn.py`의 핵심 구현(import 두 줄과 `__repr__` 세 개는 생략). 저장소 버전은 ReLU, 강의 노트북 버전은 tanh다.

```python
class Module:

    def zero_grad(self):
        for p in self.parameters():
            p.grad = 0                    # 각주: 학습 스텝마다 기울기를 0으로. 안 하면 이전 스텝 기울기에 누적됨 (+= 때문)

    def parameters(self):
        return []                         # 각주: 하위 클래스가 덮어씀. PyTorch nn.Module의 축소판

class Neuron(Module):

    def __init__(self, nin, nonlin=True):
        self.w = [Value(random.uniform(-1,1)) for _ in range(nin)]   # 각주: 입력 개수만큼 가중치. -1~1 균등분포 초기화
        self.b = Value(0)                                            # 각주: 저장소는 편향 0. 강의 노트북은 random.uniform(-1,1). 편향은 "이 뉴런이 얼마나 쉽게 발화하는가"
        self.nonlin = nonlin

    def __call__(self, x):
        act = sum((wi*xi for wi,xi in zip(self.w, x)), self.b)      # 각주: w·x + b. sum의 두 번째 인자는 시작값(b)
        return act.relu() if self.nonlin else act                    # 각주: 마지막 층은 nonlin=False로 활성 함수 생략

    def parameters(self):
        return self.w + [self.b]

class Layer(Module):

    def __init__(self, nin, nout, **kwargs):
        self.neurons = [Neuron(nin, **kwargs) for _ in range(nout)]  # 각주: 같은 입력을 보는 뉴런 nout개

    def __call__(self, x):
        out = [n(x) for n in self.neurons]
        return out[0] if len(out) == 1 else out                      # 각주: 출력이 하나면 리스트를 벗겨 스칼라로

    def parameters(self):
        return [p for n in self.neurons for p in n.parameters()]     # 각주: 뉴런들의 파라미터를 한 리스트로 펼침

class MLP(Module):

    def __init__(self, nin, nouts):
        sz = [nin] + nouts                                           # 각주: MLP(3,[4,4,1]) → sz=[3,4,4,1]
        self.layers = [Layer(sz[i], sz[i+1], nonlin=i!=len(nouts)-1) for i in range(len(nouts))]   # 각주: 마지막 층만 선형

    def __call__(self, x):
        for layer in self.layers:
            x = layer(x)                                             # 각주: 층을 차례로 통과. 이게 forward pass
        return x

    def parameters(self):
        return [p for layer in self.layers for p in layer.parameters()]
```

- **무엇**: 뉴런은 `Value` 연산의 묶음일 뿐이다. 새로운 미분 규칙이 하나도 없다. `Value`가 그래프를 알아서 만들기 때문에 뉴런, 층, MLP는 forward만 정의하면 backward가 공짜로 따라온다. 이것이 자동 미분의 핵심 이점이다.
- `MLP(3, [4, 4, 1])`의 파라미터 수: $3\cdot4+4 + 4\cdot4+4 + 4\cdot1+1 = 41$. 실행 결과 `params: 41`.
- `parameters()`를 굳이 만드는 이유는 학습 루프에서 "모든 파라미터를 한 줄로 순회"하기 위해서다. PyTorch의 `nn.Module.parameters()`와 이름까지 맞췄고, 강의에서는 `params.extend(...)` 루프를 쓰다가 중첩 리스트 컴프리헨션 한 줄로 줄인다.
- `Layer.__call__`이 출력이 하나면 리스트를 벗기는 것은 순전히 편의다. 마지막 층의 뉴런이 하나일 때 `[value]` 대신 `value`를 받으려는 것.
- 강의는 `MLP(3, [4, 4, 1])`의 forward 그래프를 `draw_dot`으로 그려 보이며 "이걸 종이에 미분할 사람은 없지만 micrograd는 끝까지 역전파할 수 있다"고 말한다.

---

## 데이터셋, loss, 학습 루프 (1:51–2:14) {#sec-training}

강의의 장난감 데이터: 입력 3차원 4개, 정답은 ±1.

```python
# 각주: 후반 노트북 cell 14(tanh Neuron/Layer/MLP), 15(n = MLP(3, [4, 4, 1])), 16, 17을 이어 붙인 것. 노트북에는 시드가 없고 이 노트의 실행은 random.seed(1337)을 추가했다
xs = [[2.0, 3.0, -1.0], [3.0, -1.0, 0.5], [0.5, 1.0, 1.0], [1.0, 1.0, -1.0]]
ys = [1.0, -1.0, -1.0, 1.0] # desired targets

for k in range(20):
  # forward pass
  ypred = [n(x) for x in xs]
  loss = sum((yout - ygt)**2 for ygt, yout in zip(ys, ypred))   # 각주: 제곱오차의 합(강의는 MSE라 부르지만 평균을 내지 않는다). 제곱하는 이유는 부호를 버리고 정답과 같을 때만 0이 되게 하려는 것. loss도 Value라 그래프에 붙는다

  # backward pass
  for p in n.parameters():
    p.grad = 0.0                                                  # 각주: zero_grad. 이걸 빼먹는 것이 강의가 강조하는 흔한 버그
  loss.backward()

  # update
  for p in n.parameters():
    p.data += -0.1 * p.grad                                       # 각주: 경사하강. 기울기 반대 방향으로 학습률 0.1만큼

  print(k, loss.data)
```

강의 노트북 코드(tanh MLP)에 `random.seed(1337)`을 추가해 이 서버에서 돌린 결과:

```
initial pred: [0.428, 0.557, 0.718, 0.452]
step 0 loss 6.0054
step 1 loss 3.2021
step 2 loss 2.4622
step 5 loss 0.7001
step 10 loss 0.0534
step 19 loss 0.0178
pred (19번째 업데이트 뒤, 마지막 backward 직전): [0.923, -0.987, -0.924, 0.923]
pred (20번째 업데이트 뒤 다시 forward): [0.926, -0.987, -0.927, 0.926]
```

정답 `[1, -1, -1, 1]`에 가까워졌다. 강의는 시드 없이 돌려 숫자는 다르지만 양상은 같다. 강의에서는 처음 만든 네트워크의 loss가 7.12였고, `parameters()`를 추가하며 재초기화한 네트워크(loss 4.84)가 첫 업데이트 뒤 4.36 → 3.9 → 3.66 → 3.47로 내려갔고, 학습률을 올리자 0.31 → 0.04까지 갔다가 **한 번 튀어 올랐다가**(overstep) 7e-9로 떨어졌다. 카파시의 설명: 우리는 loss 함수의 지역 기울기만 알 뿐 전체 모양은 모르므로, 너무 크게 밟으면 전혀 다른 곳에 떨어져 학습이 불안정해진다. 학습률은 너무 작으면 느리고 너무 크면 발산하는 "미묘한 기술"이다. 학습 루프에서는 0.01은 너무 작고 0.1은 위험하다며 그 사이 값으로 20스텝을 돌린다(공개된 노트북에는 0.1로 적혀 있다).

세 줄이 전부다. **forward(loss 계산) → zero_grad + backward(기울기) → update(파라미터 이동)**. 이 뒤에 나오는 모든 학습 코드는 이 세 줄의 변주다. 두 가지를 덧붙인다. 네 번의 forward는 같은 `n`의 파라미터를 공유하므로 전체 loss의 backward에서 각 예제가 만든 기울기가 같은 파라미터에 `+=`로 더해진다(카파시는 이 거대 그래프를 `draw_dot(loss)`로 그려 보인다. 입력 데이터에도 기울기가 생기지만 데이터는 고정이라 쓰지 않는다). 그리고 업데이트에 `-`가 붙는 이유는 기울기 벡터가 loss가 **커지는** 방향을 가리키기 때문이다. 강의에서는 `w[0].grad`가 음수인 가중치를 예로 들어, 이 값을 키우면 loss가 내려간다는 것을 먼저 확인한 뒤 부호를 정한다.

**zero_grad를 빼면**: 카파시는 학습 루프를 완성한 뒤 "인생에서 20번째로, 그것도 카메라 앞에서" 저지른 버그를 고백한다(2:10). 자신이 예전에 트윗한 "흔한 신경망 실수" 목록의 3번, backward 전에 zero grad를 잊은 것이다. `_backward`가 전부 `+=`이므로 기울기가 스텝마다 누적되어 **사실상 거대한 학습률**이 되고, 그래서 loss가 이상하게 빨리 떨어졌던 것이다. 이 문제가 너무 쉬워서 그런데도 수렴했을 뿐, 더 어려운 문제였으면 최적화가 되지 않았을 것이라고 말한다. 고친 뒤에는 더 느리지만 통제된 하강이 된다. 같은 실험을 이 서버에서 재현하면 zero_grad 없이 5스텝에 loss `0.0457`로, 역시 "우연히 잘 되는" 쪽이었다.

### `demo.ipynb`: 조금 더 진짜 같은 학습

저장소의 데모는 `sklearn`의 moons 데이터 100개, `MLP(2, [16, 16, 1])`(파라미터 337개), SVM max-margin loss, L2 정규화, 학습률 스케줄로 결정 경계를 학습한다.

```python
    # svm "max-margin" loss
    losses = [(1 + -yi*scorei).relu() for yi, scorei in zip(yb, scores)]   # 각주: hinge loss. 정답 부호로 1 이상 떨어져 있으면 loss 0. 이진 분류에는 MSE, max-margin, binary cross-entropy 모두 쓸 수 있다고 말한다
    data_loss = sum(losses) * (1.0 / len(losses))
    alpha = 1e-4
    # L2 regularization
    reg_loss = alpha * sum((p*p for p in model.parameters()))             # 각주: L2 정규화. 큰 가중치에 페널티. 카파시는 이것을 과적합 제어·일반화와 연결하고 이 영상에서는 다루지 않는다고 밝힌다
    total_loss = data_loss + reg_loss
    ...
    learning_rate = 1.0 - 0.9*k/100                                       # 각주: 학습률 감쇠. 100스텝 동안 1.0에서 0.109까지 선형 감소(식은 k=100에서 0.1). 초반엔 크게, 안정된 뒤엔 작게
```

이 서버에서 `np.random.seed(1337); random.seed(1337)`로 데모를 돌린 결과(노트북 출력과 같은 값):

```
params 337
step 0 loss 0.8958, accuracy 50.0%
step 1 loss 1.7236, accuracy 81.0%
step 2 loss 0.7429, accuracy 77.0%
step 10 loss 0.2451, accuracy 91.0%
step 50 loss 0.0988, accuracy 96.0%
step 99 loss 0.0110, accuracy 100.0%
```

---

## 강의의 요약과 GPT까지의 거리 (2:14–2:16) {#sec-summary}

카파시의 정리: 신경망은 데이터와 가중치를 입력으로 받는 수식이고, 그 뒤에 예측의 정확도를 재는 loss가 붙는다. loss를 backward해서 기울기를 얻고, 그 방향으로 파라미터를 조금 옮기는 것을 반복한다(경사하강). loss가 낮아지도록 loss를 설계했으니 loss가 낮아지면 원하는 일을 하는 것이다. GPT도 같다. 인터넷 텍스트에서 다음 단어를 맞추는 문제이고, 파라미터가 수천억 개일 뿐 `Value`와 기울기와 경사하강은 그대로다. 신경망 구조가 더 복잡하고, loss가 MSE 대신 cross-entropy이고, 단순 SGD 대신 변형된 업데이트를 쓴다는 것이 다르다.

::: {.callout-note title="minimind 대응"}
이 문단이 minimind로 가는 다리다. 주 loss는 `model_minimind.py`의 `forward` 안 `F.cross_entropy`이고(학습 루프는 여기에 MoE 보조 손실을 더하고 누적 횟수로 나눈 값을 역전파한다. 기본 dense 설정에서 보조 손실은 0), 옵티마이저는 `AdamW`다. 카파시가 "조금 다르다"고 한 것들이 정확히 그것이다.
:::

## 저장소 코드와 강의 코드의 차이 {#sec-diff}

| 항목 | 강의 노트북 | 저장소 `micrograd/` |
|---|---|---|
| 활성 함수 | `tanh` (+ `exp`) | `relu`만 |
| `Value.label` | 있음 (시각화용) | 없음 |
| 편향 초기화 | `random.uniform(-1,1)` | `Value(0)` |
| 마지막 층 | tanh 적용 | `nonlin=False`로 선형 |
| `zero_grad` | 루프 안에서 직접 | `Module.zero_grad()` |
| loss | MSE | hinge + L2 (demo) |

강의 마지막(2:16)에 카파시가 저장소 코드를 훑으며 이 차이를 설명한다. tanh를 고른 이유는 ReLU보다 매끄럽고 조금 더 복잡해서 지역 미분을 다루는 연습이 되기 때문이고, ReLU·tanh·sigmoid 사이에 "큰 차이는 없다"고 본다. `Module` 클래스는 PyTorch `nn.Module`의 API(`zero_grad`, `parameters`)를 맞추려고 둔 것이다. 데모 노트북의 배치(전체 대신 무작위 부분집합으로 forward·backward), max-margin loss, 학습률 감쇠는 워크스루에서 짧게 설명하고, L2 정규화(일반화·과적합)만 "이 영상에서는 다루지 않았다"고 밝힌다. tanh를 저장소에 추가하겠다고도 말하지만 실제로는 추가되지 않았다.

(보충) 저장소 README는 2026년에 추가된 [microgpt](https://gist.github.com/karpathy/8627fe009c40f57531cb18360106ce95)를 언급한다. micrograd 엔진을 개선해(연산마다 backward 클로저를 만드는 대신 forward 때 지역 기울기를 저장) 의존성 없는 순수 파이썬으로 GPT-2 스타일 transformer를 학습하는 단일 파일이다. 이 시리즈를 끝낸 뒤 읽으면 좋은 다음 단계다.

::: {.callout-note title="minimind 대응"}
minimind에는 micrograd에 해당하는 코드가 없다. PyTorch autograd가 전부 대신한다. 대응 관계는 이렇다.

| micrograd | minimind (`trainer/train_pretrain.py`) |
|---|---|
| `Value` | `torch.Tensor` (`requires_grad=True`인 파라미터) |
| `loss.backward()` | `scaler.scale(loss).backward()` — `scaler.scale`은 float16 학습용 loss scaling. 기본 bfloat16 설정에서는 비활성이고 혼합 정밀도는 `autocast`가 담당 |
| `for p in parameters(): p.grad = 0` | `optimizer.zero_grad(set_to_none=True)` — 0 대신 `None`으로 둔다(보충: 메모리·속도상 이점) |
| `p.data += -lr * p.grad` | `scaler.step(optimizer)` — AdamW가 단순 경사하강 대신 모멘텀·적응 학습률로 이동 |
| 없음 | `clip_grad_norm_(model.parameters(), args.grad_clip)` — 기본 1.0. 기울기 폭발 방지 |
| `Neuron`/`Layer`/`MLP` | `model_minimind.py`의 `FeedForward`: 편향 없는 선형 변환 세 개(gate, up, down). `down_proj(silu(gate_proj(x)) * up_proj(x))`, 즉 gate 쪽에 SiLU($z\sigma(z)$)를 씌워 up 쪽과 원소별로 곱하는 SwiGLU. `Layer`가 편향 있는 뉴런 한 줄이라면 이쪽은 게이팅이 있는 두 갈래 구조다 |
| `relu` / `tanh` | `silu` (`config.hidden_act`) |
| `Module.parameters()` | `nn.Module.parameters()` |

micrograd의 학습 루프 세 줄이 `train_pretrain.py`의 `train_epoch`에 있지만 순서와 주기가 다르다. forward와 backward는 microbatch마다 하고, 기본 8번 누적한 뒤에야 `unscale → clip → step → zero_grad`를 한다. 즉 zero_grad가 backward 앞이 아니라 업데이트 뒤에 오고, 그 사이 기울기는 의도적으로 `+=` 누적된다. 카파시가 버그로 보여준 "기울기 누적"을 통제된 형태로 쓰는 셈이다. 그 밖에 혼합 정밀도, 학습률 스케줄, 체크포인트가 끼어 있다.
:::

---

## 직접 볼 때 집중할 구간

| 구간 | 이유 |
|---|---|
| 0:19–0:32 | graphviz로 그래프를 그리고 노드에 값을 채워 넣는 과정. 이 노트의 그림은 완성된 정적 그래프 하나뿐이다 |
| 0:32–0:53 | 손으로 기울기를 채우는 과정. 표만 보지 말고 카파시가 각 칸을 채울 때 멈추고 직접 계산해 볼 것 |
| 1:22–1:27 | `a + a` 버그를 실제로 겪는 장면 |
| 1:31, 1:34 | "영상을 멈추고 직접 생각해 보라"는 두 지점: `exp`와 `pow`의 `_backward` |
| 2:04–2:08 | 학습률을 올리다가 loss가 튀어 오르는(overstep) 장면 |
| 2:10–2:13 | zero_grad를 빼먹은 버그를 고백하고 고치는 장면 |
| 2:21–2:25 | PyTorch 소스 안의 tanh backward를 찾아가는 장면. 자막으로는 코드가 안 보인다 |

## 이해 확인 질문

1. `__mul__`의 `_backward`에서 `self.grad += other.data * out.grad`의 세 항이 각각 무엇을 뜻하는가? 연쇄법칙의 어느 부분인가?
2. `backward()`에서 위상 정렬을 뒤집어 순회하는 이유는? `a = Value(3.0); b = a * 2; c = b * 4`에서 `reversed(topo)` 대신 `topo` 순서로 `_backward`를 부르면 `a.grad`, `b.grad`는 각각 얼마가 되는가? (정상은 8, 4)
3. `a = Value(3.0); b = a * a; b.backward()`에서 `a.grad`는 얼마여야 하는가? `_backward`가 `+=`가 아니라 `=`이면 얼마가 나오는가? (본문의 `a + a`를 곱셈으로 바꿔 생각하라)
4. 학습 루프에서 `p.grad = 0`을 빼먹으면 두 번째 스텝의 `p.grad`에는 무엇이 들어 있는가?
5. minimind의 `FeedForward`는 micrograd의 `Layer`와 무엇이 같고 무엇이 다른가? (힌트: gate/up/down 세 행렬, SwiGLU, 편향 없음)

## 실습으로 이어지는 지점

- 저장소를 clone해 `python -m pytest`로 PyTorch와 일치하는지 확인한 뒤, `engine.py`에 `tanh`와 `exp`를 직접 추가하고 테스트를 넓혀 보기.
- 설명란의 연습문제 Colab 풀기.
- `model_minimind.py`의 `FeedForward`를 micrograd `Value`로 다시 써 보기 (입력 2차원, hidden 3으로 축소). SwiGLU의 `_backward`가 어떻게 조합되는지 그래프로 그려 보기.
- minimind `train_pretrain.py`의 `train_epoch`에서 micrograd의 세 줄(forward, zero_grad+backward, update)에 해당하는 줄을 찾아 표시하기.
