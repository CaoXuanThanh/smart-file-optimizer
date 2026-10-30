import sys, csv, io
from pathlib import Path
from time import perf_counter

sys.path.insert(0, str(Path(__file__).parent / "src"))
import streamlit as st
from smartfile.core import top_k, readable
from smartfile.operations import process

st.set_page_config(page_title="Smart File Optimizer", page_icon="🗂️", layout="wide")
st.markdown(
    """<style>.block-container{max-width:1150px;padding-top:2rem}.hero{background:linear-gradient(110deg,#101a36,#115e59);border-radius:22px;padding:32px 36px;color:white}.hero h1{color:white;margin:0;font-size:2.6rem}.hero p{color:#ccfbf1;margin-bottom:0}[data-testid="stMetric"]{border:1px solid #5c728455;border-radius:13px;padding:13px}</style>""",
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero"><h1>Smart File Optimizer</h1><p>Find the big files. Make smarter space decisions. · Top-K Min-Heap + Huffman</p></div>',
    unsafe_allow_html=True,
)
st.caption("CTDL & GT · Python · Chạy cục bộ · Không sửa, xóa hoặc ghi đè file có sẵn")
a, b, c = st.tabs(["📊 TOP-K EXPLORER", "🗜️ HUFFMAN LAB", "📘 ABOUT"])
with a:
    col1, col2 = st.columns([4, 1])
    with col1:
        folder = st.text_input("Đường dẫn thư mục", value=str(Path.home()))
    with col2:
        k = st.number_input("Số file (K)", min_value=1, max_value=10000, value=10)
    if st.button("🔎 Scan folder", type="primary", width="stretch"):
        try:
            with st.spinner("Đang quét thư mục…"):
                t = perf_counter()
                rows, n, errs = top_k(folder, int(k))
                st.session_state["scan"] = (rows, n, errs, perf_counter() - t)
        except (OSError, ValueError) as exc:
            st.session_state.pop("scan", None)
            st.error(str(exc))
    if "scan" in st.session_state:
        rows, n, errs, seconds = st.session_state["scan"]
        x, y, z = st.columns(3)
        x.metric("File scanned", f"{n:,}")
        y.metric("Top files", len(rows))
        z.metric("Scan time", f"{seconds:.3f}s")
        records = [
            {
                "Rank": i,
                "Name": Path(p).name,
                "Size": readable(s),
                "Bytes": s,
                "Path": p,
            }
            for i, (s, p) in enumerate(rows, 1)
        ]
        if records:
            st.dataframe(records, hide_index=True, width="stretch")
            st.bar_chart(
                {f"{Path(p).name} #{i}": s for i, (s, p) in enumerate(rows[:12], 1)},
                horizontal=True,
            )
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=list(records[0]))
            writer.writeheader()
            writer.writerows(records)
            st.download_button(
                "Export CSV",
                output.getvalue().encode("utf-8-sig"),
                "top_k.csv",
                "text/csv",
            )
        else:
            st.info("Không tìm thấy file nào.")
        if errs:
            st.warning(f"Bỏ qua {len(errs)} đường dẫn không truy cập được.")
            st.code("\n".join(errs[:10]))
with b:
    st.info(
        "Huffman không mất dữ liệu nhưng có thể làm file lớn hơn; đây là định dạng .huf riêng, không phải WinRAR/ZIP."
    )
    mode = st.radio("Chế độ", ["Nén file", "Giải nén file"], horizontal=True)
    source = st.text_input("Đường dẫn file nguồn", key="source")
    dest = st.text_input("Đường dẫn file đích (phải chưa tồn tại)", key="destination")
    if st.button("▶ Start", type="primary"):
        try:
            with st.spinner("Đang xử lý và kiểm tra dữ liệu…"):
                result = process(
                    "compress" if mode == "Nén file" else "decompress", source, dest
                )
            st.success("Hoàn thành. Không ghi đè file gốc.")
            st.json(result)
        except (OSError, ValueError) as exc:
            st.error(str(exc))
with c:
    st.markdown(
        """### Min-Heap Top-K
Quét N file nhưng chỉ giữ K bản ghi. Gốc của Min-Heap là file nhỏ nhất trong nhóm Top-K; gặp file lớn hơn thì thay gốc. **O(N log K)** thời gian, **O(K)** bộ nhớ phụ cho khâu chọn file.

### Huffman
Thống kê tần suất byte → ghép hai nút có tần suất nhỏ nhất → tạo cây mã tiền tố → mã hóa bit → lưu header để giải nén. Nén không đồng nghĩa mã hóa mật khẩu.

### Limitations
Huffman xử lý theo khối 64 KiB qua hai lượt đọc. HUF2 kiểm tra SHA-256, HUF1 cũ không có checksum. Giới hạn giải nén mặc định 1 GiB. File đích có thể xuất hiện trong khi ghi, chỉ sử dụng sau thông báo thành công. Chỉ xử lý file cục bộ. Không tự động xóa/ghi đè hay bảo đảm file nén nhỏ hơn."""
    )
