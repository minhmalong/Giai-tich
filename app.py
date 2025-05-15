# haman.py
import streamlit as st
import sympy as sp

# 1) Khai báo các symbol
beta1, beta2, beta3, beta4, beta5, beta6 = sp.symbols(
    'beta1 beta2 beta3 beta4 beta5 beta6', real=True
)
X1, X2, X3, X4, X5, X6 = sp.symbols(
    'X1 X2 X3 X4 X5 X6', positive=True
)
f1, f2 = sp.symbols('f1 f2', real=True)
dX3, dX4, dX5, dX6 = sp.symbols('dX3 dX4 dX5 dX6', real=True)

# 2) Phương trình cân bằng
expr = beta1*f1 + beta2*f2 + beta3*dX3 + beta4*dX4 + beta5*dX5 + beta6*dX6

# 3) Các giá trị beta cho trước
beta_vals = {
    beta1: -0.49187, beta2: 0.94001,
    beta3: 0.00987,  beta4: -0.02334,
    beta5: 0.09802,  beta6: 0.01616,
}
st.sidebar.header("🔧 Hệ số β (cố định)")
for i, b in enumerate([beta1,beta2,beta3,beta4,beta5,beta6], start=1):
    st.sidebar.write(f"β{i} = {beta_vals[b]:.5f}")

# 4) Cho người dùng nhập giá trị gốc X
st.sidebar.header("🔧 Giá trị gốc Xi")
base = {}
for Xi, lbl in zip([X1,X2,X3,X4,X5,X6], ['X1','X2','X3','X4','X5','X6']):
    base[Xi] = st.sidebar.number_input(f"{lbl} (gốc)", value=100.0)

# 5) Cho người dùng nhập thay đổi của dX
st.sidebar.header("✏️ Thay đổi ban đầu")
f1_val = st.sidebar.number_input("dX1/X1", value=0.00, step=0.01)
f2_val = st.sidebar.number_input("dX2/X2", value=0.00, step=0.01)
dvals = {
    dX3: st.sidebar.number_input("dX3", value=0.00, step=0.1),
    dX4: st.sidebar.number_input("dX4", value=0.00, step=0.1),
    dX5: st.sidebar.number_input("dX5", value=0.00, step=0.1),
    dX6: st.sidebar.number_input("dX6", value=0.00, step=0.1),
}

# 6) Tính giá trị hiện tại
subs0 = {**beta_vals, f1: f1_val, f2: f2_val, **dvals}
current = float(expr.subs(subs0))
current_display = 0.0 if abs(current) < 1e-6 else current
st.title("Đạo hàm hàm ẩn — Cobb–Douglas")
st.markdown("#### 📐 Phương trình cân bằng:")
st.latex(r"\beta_1\,\frac{dX_1}{X_1} + \beta_2\,\frac{dX_2}{X_2} + \beta_3\,dX_3 + \beta_4\,dX_4 + \beta_5\,dX_5 + \beta_6\,dX_6 = 0")
st.write(f"**Giá trị hiện tại:** {current_display:+.6f}")

# 7) Nếu khác 0 thì cho người dùng chọn biến
if abs(current_display) > 1e-9:
    st.warning("Biểu thức ≠ 0 — chọn biến để điều chỉnh:")
    sel = st.selectbox("👉 Chọn biến", ["dX1/X1","dX2/X2","dX3","dX4","dX5","dX6"])

    # Tính toán
    fixed = {**beta_vals}
    if sel == "dX1/X1":
        target = f1
        fixed.update({f2: f2_val, **dvals})
    elif sel == "dX2/X2":
        target = f2
        fixed.update({f1: f1_val, **dvals})
    else:
        target = {'dX3':dX3,'dX4':dX4,'dX5':dX5,'dX6':dX6}[sel]
        fixed.update({f1: f1_val, f2: f2_val, **dvals})
        fixed.pop(target)

    sol = sp.solve(expr.subs(fixed), target)
    if not sol:
        st.error("Không tìm được nghiệm.")
    else:
        new_val = float(sol[0])
      
        if sel in ("dX1/X1","dX2/X2"):
            var = '1' if sel=='dX1/X1' else '2'
            orig = f1_val if sel=='dX1/X1' else f2_val
            st.latex(rf"{{dX_{{{var}}}}}{{/X_{{{var}}}}}^{{new}} = {new_val:.4f}")
            st.markdown(rf"**Vậy** dX{var} từ {orig:+.4f} tới **{new_val:+.4f}** để cân bằng.")

   
        else:
            var = sel[-1]
            orig = dvals[target]
            st.latex(rf"\Delta X_{{{var}}}^{{new}} = {new_val:.4f}")
            st.markdown(rf"**Vậy** dX{var} từ {orig:+.4f} tới **{new_val:+.4f}** để cân bằng.")
else:
    st.success("🎉 Đã cân bằng — không cần điều chỉnh.")

st.caption("Nhóm 10")
