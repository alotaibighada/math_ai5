import streamlit as st
from sympy import symbols, Eq, solve, sympify

# إعداد الصفحة
st.set_page_config(page_title="Math AI – البرنامج الحسابي", layout="centered")

# CSS لتحسين الواجهة
st.markdown("""
<style>
.stNumberInput>div>div>input, .stTextInput>div>div>input {
    background: rgba(240,240,240,1);
    color: black;
    font-size: 1.2em;
    padding: 0.5em;
    border-radius: 5px;
    border: 1px solid #ccc;
    text-align: center;
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    height: 3em;
    width: 100%;
    border-radius: 8px;
    border: none;
    font-weight: bold;
    font-size: 1.2em;
}
.op-buttons button {
    padding: 0.5em 1em;
    margin: 0.2em;
    border-radius: 5px;
    font-size: 1.1em;
    font-weight: bold;
    color: white;
    border: none;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

st.title("Math AI – البرنامج الحسابي 🧮")
st.markdown("أدخل الرقمين، اختر العملية الحسابية، أو اكتب معادلة لحلها.")

# سجل العمليات السابقة
if 'history' not in st.session_state:
    st.session_state.history = []

# -----------------------------
# القسم الأول: العمليات الحسابية
# -----------------------------
st.header("العمليات الحسابية الأساسية")

col1, col2 = st.columns(2)
num1 = col1.number_input("الرقم الأول:", value=0)
num2 = col2.number_input("الرقم الثاني:", value=0)

# أزرار العمليات
operations = {"جمع": "+", "طرح": "-", "ضرب": "×", "قسمة": "÷"}
col_op1, col_op2, col_op3, col_op4 = st.columns(4)
op_selected = None
for col, (op_name, symbol) in zip([col_op1, col_op2, col_op3, col_op4], operations.items()):
    if col.button(op_name):
        op_selected = op_name

if op_selected:
    result = None
    symbol = operations[op_selected]
    if op_selected == "جمع":
        result = num1 + num2
    elif op_selected == "طرح":
        result = num1 - num2
    elif op_selected == "ضرب":
        result = num1 * num2
    elif op_selected == "قسمة":
        if num2 != 0:
            result = num1 / num2
        else:
            st.error("❌ لا يمكن القسمة على صفر")
    
    if result is not None:
        st.success(f"✅ {num1} {symbol} {num2} = {result}")
        st.session_state.history.append(f"{num1} {symbol} {num2} = {result}")

# -----------------------------
# القسم الثاني: حل المعادلات
# -----------------------------
st.header("حل المعادلات البسيطة")
user_input = st.text_input("اكتب المعادلة هنا (مثال: 2*x + 5 = 15)")

x = symbols('x')
if user_input:
    try:
        if '=' in user_input:
            lhs, rhs = user_input.split('=')
            equation = Eq(sympify(lhs.strip()), sympify(rhs.strip()))
            solution = solve(equation, x)
            st.success(f"✅ حل المعادلة: {solution}")
            st.session_state.history.append(f"{user_input} => {solution}")
        else:
            result = sympify(user_input).evalf()
            st.success(f"✅ الناتج: {result}")
            st.session_state.history.append(f"{user_input} = {result}")
    except Exception as e:
        st.error(f"❌ خطأ في المسألة: {e}")

# -----------------------------
# سجل العمليات والأزرار
# -----------------------------
if st.session_state.history:
    st.subheader("📜 سجل العمليات السابقة")
    for idx, item in enumerate(reversed(st.session_state.history), 1):
        st.write(f"{idx}. {item}")

col_reset, col_clear = st.columns(2)
if col_reset.button("🔄 إعادة تعيين الإدخالات"):
    st.experimental_rerun()
if col_clear.button("🗑️ مسح سجل النتائج"):
    st.session_state.history = []
    st.experimental_rerun()
