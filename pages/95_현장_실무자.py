"""
현장 실무자 검토 — 단일 수직 스크롤 페이지 (최종)
상단 anchor 탭 네비게이션 / 모든 섹션 수직 배치
"""

import streamlit as st
from planner import apply_wireframe_theme, page_header

PAGE_TITLE = "현장 실무자 검토"

# ─────────────────────────────────────────────
# Mock 데이터
# ─────────────────────────────────────────────
RECENT_COMPANIES = [
    {"color": "#1a73e8", "기업명": "삼성전자",       "산업군": "반도체 / 전기전자",  "최근검색일": "2026.03.17 09:30", "상태코드": "green",  "예상계약규모": "15억 원"},
    {"color": "#34a853", "기업명": "네이버 (NAVER)", "산업군": "IT 플랫폼 / 서비스", "최근검색일": "2026.03.16 15:42", "상태코드": "orange", "예상계약규모": "3억 5,000만 원"},
    {"color": "#202124", "기업명": "현대자동차",      "산업군": "자동차 / 운송장비",  "최근검색일": "2026.03.15 11:20", "상태코드": "gray",   "예상계약규모": "미정"},
    {"color": "#fbbc04", "기업명": "카카오",          "산업군": "IT 플랫폼 / 서비스", "최근검색일": "2026.03.14 18:05", "상태코드": "green",  "예상계약규모": "8억 원"},
    {"color": "#ea4335", "기업명": "SK하이닉스",      "산업군": "반도체",             "최근검색일": "2026.03.12 10:15", "상태코드": "blue",   "예상계약규모": "12억 원"},
]

STATUS_BADGE = {
    "green":  ("계약 완료", "#1e7e34", "#d4edda"),
    "orange": ("검토 중",   "#856404", "#fff3cd"),
    "gray":   ("검토 대기", "#495057", "#e2e3e5"),
    "blue":   ("진행 중",   "#0c5460", "#d1ecf1"),
}

COMPANY_DB = {
    "SK 주식회사": {
        "회사명": "SK 주식회사", "기본 계약": "있음", "계약 상태": "활성",
        "기본계약명": "부품공급 기본계약", "담당부서": "전장소재구매팀",
        "체결일": "2024-03-15", "만료일": "2027-03-14",
    },
    "에이아이테크": {
        "회사명": "에이아이테크", "기본 계약": "없음", "계약 상태": "미체결",
        "기본계약명": "-", "담당부서": "신사업부", "체결일": "-", "만료일": "-",
    },
}

COMPANY_DETAIL = {
    "SK 주식회사": {
        "소재지": "서울특별시 종로구 종로 26", "設立年月日": "1953-04-08",
        "資本金": "3,657억 원", "代表者名": "최태원", "従業員数": "3,500명",
        "事業内容": "에너지, 화학, ICT, 반도체 소재", "主要株主": "최태원 외",
        "主要取引銀行": "우리은행, 신한은행", "グループ会社": "SK그룹",
        "Webサイト": "www.sk.com", "評点": "AAA",
    }
}

MOCK_OCR = {
    "기업명": "(주) 에이아이테크", "대표자": "홍길동", "직급/직함": "본부장",
    "주소": "경기도 분당", "연락처": "02-1234-1234", "이메일": "abcd@aaaa",
}

MOCK_RISKS = [
    {
        "no": 1, "title": "손해배상 상한",
        "bullets": [">배상 상한 100% 제한", ">문구가 삭제됨"],
        "highlight": "제12조 ② 항 — '손해배상의 범위는 직접 손해로 한정하며, 총 계약금액의 100%를 초과할 수 없다'는 문구가 현 계약서에서 누락되어 있습니다.",
        "source": "표준계약서 제12조 제2항 vs 현 계약서 제12조",
    },
    {
        "no": 2, "title": "지연배상률 상향",
        "bullets": [">월 0.5% 제한 대신 월 2%로 상향됨"],
        "highlight": "제15조 — 지연배상금 산정 기준이 표준 대비 월 0.5%에서 월 2%로 4배 높게 설정되어 있어 재무 리스크가 존재합니다.",
        "source": "표준계약서 제15조 제1항",
    },
    {
        "no": 3, "title": "불가항력 조항 축소",
        "bullets": [">천재지변만 인정되고", ">정책변경/전염병이 제외됨"],
        "highlight": "제20조 — 불가항력 사유가 '천재지변'으로만 한정되어 있으며, 코로나19와 같은 전염병이나 정부 정책 변경은 면책 사유에서 제외됩니다.",
        "source": "표준계약서 제20조 불가항력 정의 조항",
    },
]

FAQ_CHIPS = [
    "기본계약 없는 경우 어떻게 진행하나요?",
    "현재 문서에서 가장 큰 리스크는 무엇인가요?",
    "스캔본 PDF가 올라오면 어떻게 되나요?",
    "지연배상률 조정 기준이 있나요?",
    "선지급 조건은 어떻게 판단하나요?",
]

FAQ_ANSWERS = {
    "기본계약 없는 경우 어떻게 진행하나요?":
        "기본계약이 없는 경우 개별 계약 체결을 우선 진행하며, 거래 규모가 일정 기준을 초과할 경우 법무팀 검토 후 기본계약 체결을 권고합니다.",
    "현재 문서에서 가장 큰 리스크는 무엇인가요?":
        "현재 분석된 문서에서 가장 큰 리스크는 '손해배상 상한' 조항 누락입니다. 배상 상한이 없으면 계약금액을 초과하는 손해배상 청구가 가능합니다.",
    "스캔본 PDF가 올라오면 어떻게 되나요?":
        "스캔본 PDF는 텍스트 추출이 불가하여 '추출 실패'로 처리됩니다. Textable PDF 또는 Word 변환 후 업로드를 권장합니다.",
    "지연배상률 조정 기준이 있나요?":
        "국내 표준 기준은 월 0.5~1%이며, 월 1% 초과 시 협상을 통해 조정 요청이 가능합니다. 법무팀 가이드라인 참고가 필요합니다.",
    "선지급 조건은 어떻게 판단하나요?":
        "신용정보와 현금흐름을 함께 확인하고, 20%를 초과하는 선지급 요구는 별도 승인 트리거로 분류합니다.",
}

SOURCE_DB = {
    "SRC-107": {
        "tags": ["SRC-107", "근거 확인"],
        "문서명": "거래처 신용리포트",
        "조항": "재무요약",
        "내용": "현금흐름 변동성 증가, 선지급 조건 주의 필요.",
    },
    "SRC-042": {
        "tags": ["SRC-042", "계약 표준"],
        "문서명": "표준계약서 가이드라인",
        "조항": "제12조 손해배상",
        "내용": "손해배상 상한은 총 계약금액의 100%로 제한함이 표준 원칙.",
    },
}

# ─────────────────────────────────────────────
# Session state 초기화
# ─────────────────────────────────────────────
_defaults = {
    "show_search_ui": False,
    "search_term": "",
    "found_company": None,
    "show_kigyou": False,
    "contract_uploaded": False,
    "contract_filename": "",
    "contract_type": "기본 계약",
    "show_review_modal": False,
    "field_opinion": "",
    "review_comment": "",
    "review_priority": "High",
    "review_id": "",
    "qna_history": [],
    "show_source_modal": False,
    "source_modal_key": "",
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

st.set_page_config(page_title=PAGE_TITLE, layout="wide")

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── 자동 스크롤 완전 차단 ── */
html { scroll-behavior: auto !important; }
[data-testid="stAppViewContainer"] { overflow-anchor: none; }

/* ── 페이지 제목 (h1) ── */
h1 {
    font-size: 2.6rem !important;
    font-weight: 900 !important;
    background: linear-gradient(90deg, #1a4e8f 0%, #c0392b 55%, #16a085 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.5px;
}

/* ── 섹션 제목 (h2) ── */
h2 {
    font-size: 1.45rem !important;
    font-weight: 800 !important;
    color: #1a4e8f !important;
    border-left: 5px solid #c0392b;
    padding-left: 12px;
    margin-bottom: 16px !important;
}

/* 상단 anchor 탭 네비게이션 */
.nav-bar {
    display: flex;
    gap: 0;
    margin-bottom: 28px;
    border-bottom: 2px solid #b8a890;
    padding-bottom: 0;
}
.nav-bar a {
    text-decoration: none;
    color: #666;
    font-size: 14px;
    padding: 8px 22px;
    border-radius: 6px 6px 0 0;
    font-weight: 500;
    border: 1px solid transparent;
    margin-bottom: -2px;
}
.nav-bar a:hover {
    background: #ede3d6;
    color: #222;
}
.nav-bar a.active {
    background: #f5ede2;
    color: #111;
    font-weight: 700;
    border: 1px solid #b8a890;
    border-bottom: 2px solid #f5ede2;
}

/* 섹션 구분 */
.section-divider {
    border: none;
    border-top: 2px solid #c8b99a;
    margin: 48px 0 32px 0;
}

/* 계약상태 배지 */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 3px 10px;
    border-radius: 14px;
    font-size: 12px;
    font-weight: 600;
    white-space: nowrap;
}

/* 회사 컬러 아이콘 */
.co-dot {
    display: inline-block;
    width: 13px; height: 13px;
    border-radius: 3px;
    vertical-align: middle;
}

/* SRC 배지 */
.src-tag {
    display: inline-block;
    border: 1px solid #999;
    border-radius: 6px;
    padding: 2px 9px;
    font-size: 12px;
    color: #444;
    margin-top: 4px;
    cursor: pointer;
}

/* FAQ 칩 버튼 커스텀 — streamlit 기본 버튼이라 CSS 제한적 */
div[data-testid="stHorizontalBlock"] button {
    white-space: normal;
    text-align: left;
}

/* 리스크 카드 번호 */
.risk-no {
    display: inline-block;
    width: 22px; height: 22px;
    background: #555;
    color: #fff;
    border-radius: 50%;
    text-align: center;
    line-height: 22px;
    font-size: 12px;
    font-weight: 700;
    margin-right: 6px;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 상단 anchor 네비게이션
# ─────────────────────────────────────────────
def _nav():
    st.markdown("""
    <div class="nav-bar">
      <a href="#sec-company" class="active">거래처 정보</a>
      <a href="#sec-contract">계약서 업로드 및 표준 비교</a>
      <a href="#sec-ai">AI 리스크 검토</a>
      <a href="#sec-qna">실무 Q&A</a>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SECTION 1 — 거래처 정보
# ─────────────────────────────────────────────
def section_company():
    st.markdown('<a name="sec-company"></a>', unsafe_allow_html=True)

    if not st.session_state["show_search_ui"]:
        _company_landing()
    else:
        _company_search()


def _company_landing():
    """거래처 목록 테이블 랜딩"""
    # 테이블 헤더
    h = st.columns([0.35, 2.1, 1.8, 1.8, 1.5, 1.5])
    for col, lbl in zip(h, ["", "기업명", "산업군", "최근 검색일", "계약 상태", "예상 계약 규모"]):
        col.markdown(f"<span style='font-size:13px; color:#777;'>{lbl}</span>", unsafe_allow_html=True)

    with st.container(border=True):
        for co in RECENT_COMPANIES:
            sc = co["상태코드"]
            label, txt_color, bg_color = STATUS_BADGE[sc]

            # 아이콘별 prefix
            icon_map = {"green": "✅", "orange": "💬", "gray": "🔵", "blue": "🔄"}
            icon = icon_map.get(sc, "")

            row = st.columns([0.35, 2.1, 1.8, 1.8, 1.5, 1.5])
            with row[0]:
                st.markdown(
                    f'<span class="co-dot" style="background:{co["color"]};"></span>',
                    unsafe_allow_html=True,
                )
            with row[1]:
                st.markdown(f"**{co['기업명']}**")
            with row[2]:
                st.write(co["산업군"])
            with row[3]:
                st.write(co["최근검색일"])
            with row[4]:
                st.markdown(
                    f'<span class="status-badge" style="background:{bg_color}; color:{txt_color};">'
                    f'{icon} {label}</span>',
                    unsafe_allow_html=True,
                )
            with row[5]:
                st.write(co["예상계약규모"])

    st.markdown("")
    _, cta_col, _ = st.columns([1, 2, 1])
    with cta_col:
        if st.button("신규 거래처 검색", key="btn_new_search", use_container_width=True):
            st.session_state["show_search_ui"] = True
            st.rerun()


def _company_search():
    """신규 거래처 검색 화면"""
    if st.button("← 거래처 목록으로", key="btn_back"):
        st.session_state["show_search_ui"] = False
        st.session_state["search_term"] = ""
        st.session_state["found_company"] = None
        st.session_state["show_kigyou"] = False
        st.rerun()

    st.markdown("")

    # 검색 박스 — 좌: 거래처명 검색 / 우: 명함 이미지 업로드 / 하단 중앙: 기업 정보 표시
    with st.container(border=True):
        col_search_area, col_divider, col_card_area = st.columns([5, 0.15, 4])

        # ── 좌측: 거래처명 텍스트 검색 ──
        with col_search_area:
            st.markdown(
                "<div style='font-size:14px; font-weight:700; color:#1a4e8f; margin-bottom:8px;'>"
                "🔍 거래처 검색</div>",
                unsafe_allow_html=True,
            )
            col_in, col_srch = st.columns([3, 1])
            with col_in:
                search_input = st.text_input(
                    "거래처명",
                    value=st.session_state["search_term"],
                    placeholder="거래처명을 입력하세요",
                    label_visibility="collapsed",
                    key="search_field",
                )
            with col_srch:
                search_clicked = st.button("검색 >", key="btn_search", use_container_width=True)

        # ── 구분선 ──
        with col_divider:
            st.markdown(
                "<div style='border-left:1px dashed #bbb; height:80px; margin-top:18px;'></div>",
                unsafe_allow_html=True,
            )

        # ── 우측: 명함 이미지 업로드 ──
        with col_card_area:
            st.markdown(
                "<div style='font-size:14px; font-weight:700; color:#1a4e8f; margin-bottom:8px;'>"
                "📷 명함 이미지 업로드</div>",
                unsafe_allow_html=True,
            )
            card_img = st.file_uploader(
                "명함 이미지",
                type=["png", "jpg", "jpeg"],
                key="card_img_search",
                label_visibility="collapsed",
                help="명함 이미지를 드래그하거나 클릭해서 업로드하세요.",
            )
            if card_img:
                st.session_state["card_img_uploaded"] = True
                ocr_name = MOCK_OCR.get("기업명", "").replace("(주) ", "")
                if ocr_name not in st.session_state.get("_card_search_done", ""):
                    st.session_state["_card_search_done"] = ocr_name

        # ── 하단 중앙: 기업 정보 표시 버튼 ──
        st.markdown("")
        _, show_col, _ = st.columns([2, 2, 2])
        with show_col:
            show_clicked = st.button(
                "기업 정보 표시", key="btn_show_info", use_container_width=True
            )

    # 검색 트리거 처리
    if search_clicked:
        t = search_input.strip()
        if t:
            st.session_state["search_term"] = t
            st.session_state["found_company"] = COMPANY_DB.get(t)
            st.session_state["show_kigyou"] = False
            st.rerun()

    if show_clicked:
        t = search_input.strip()
        if t:
            st.session_state["search_term"] = t
            st.session_state["found_company"] = COMPANY_DB.get(t)
            # 기업 정보 표시 = 企業調査 패널 열기
            st.session_state["show_kigyou"] = True
            st.rerun()

    # 명함 이미지 업로드 시 OCR 결과 표시
    if "card_img_search" in st.session_state and st.session_state.get("_card_search_done"):
        ocr_company = st.session_state["_card_search_done"]
        st.markdown("---")
        st.markdown(
            "<div style='font-size:13px; font-weight:700; color:#555; margin-bottom:6px;'>"
            "📋 명함 OCR 인식 결과</div>",
            unsafe_allow_html=True,
        )
        with st.container(border=True):
            for k, v in MOCK_OCR.items():
                st.write(f"{k} : {v}")

        col_use, col_ignore = st.columns(2)
        with col_use:
            if st.button("이 정보로 거래처 검색", key="btn_ocr_to_search", use_container_width=True):
                st.session_state["search_term"] = ocr_company
                st.session_state["found_company"] = COMPANY_DB.get(ocr_company)
                st.session_state["show_kigyou"] = False
                st.session_state["_card_search_done"] = ""
                st.rerun()
        with col_ignore:
            if st.button("무시하고 직접 입력", key="btn_ocr_ignore", use_container_width=True):
                st.session_state["_card_search_done"] = ""
                st.rerun()
        return  # OCR 결과 표시 중엔 아래 검색결과 렌더 스킵

    term  = st.session_state["search_term"]
    found = st.session_state["found_company"]

    if not term:
        st.caption("예: SK 주식회사  /  에이아이테크")
        return

    has_contract = bool(found and found.get("기본 계약") == "있음")

    st.markdown("")

    if found and has_contract:
        # 기본 계약 있음 → "기업 정보 표시" 클릭 시 企業調査 내용 표시
        with st.container(border=True):
            st.markdown("**기본 계약 : 있음**")
            st.markdown("---")
            for key in ("계약 상태", "기본계약명", "담당부서", "체결일", "만료일"):
                st.write(f"{key} : {found[key]}")

        if st.session_state["show_kigyou"]:
            _kigyou_modal(found["회사명"])

    else:
        # 기본 계약 없음 → 명함 업로드 인라인
        if found:
            st.warning(f"**{found['회사명']}** — 기본 계약이 없습니다.")
        else:
            st.warning(f"**'{term}'** — 등록된 기업을 찾을 수 없습니다.")

        with st.container(border=True):
            _, badge_col, _ = st.columns([1, 2, 1])
            with badge_col:
                st.markdown(
                    "<div style='text-align:center; font-size:16px; font-weight:700; "
                    "border:1px solid #aaa; border-radius:8px; padding:8px;'>기본 계약 : 없음</div>",
                    unsafe_allow_html=True,
                )
            st.markdown("")
            _card_upload_inline()


def _kigyou_modal(company_name: str):
    """企業調査 팝업 (expander 기반, 다크 배경 연출)"""
    import pandas as pd
    detail = COMPANY_DETAIL.get(company_name, {})

    with st.expander("📋 企業調査 — 기업 상세 정보", expanded=True):
        _, close_col = st.columns([9, 1])
        with close_col:
            if st.button("✕", key="btn_close_kigyou"):
                st.session_state["show_kigyou"] = False
                st.rerun()

        st.markdown("**1. 基本情報**")
        for k, v in {"会社名": company_name, **detail}.items():
            c1, c2 = st.columns([2, 3])
            c1.write(k)
            c2.markdown(f'<input type="text" value="{v}" '
                        'style="width:100%; border:1px solid #ccc; border-radius:4px; '
                        'padding:3px 6px; background:#fff;" readonly>',
                        unsafe_allow_html=True)

        st.markdown("")
        st.markdown("**2. 財務情報 (最近3期, 단위: 円)**")
        fin_df = pd.DataFrame({
            "年度":       ["2022", "2023", "2024"],
            "売上高":     ["18,200", "19,500", "21,300"],
            "営業利益":   ["1,820",  "2,100",  "2,430"],
            "経常利益":   ["1,700",  "1,980",  "2,200"],
            "当期純利益": ["1,200",  "1,400",  "1,600"],
            "総資産":     ["42,000", "44,500", "47,000"],
            "純資産":     ["15,000", "16,200", "17,400"],
        })
        st.dataframe(fin_df, use_container_width=True, hide_index=True)


def _card_upload_inline():
    """명함 업로드 + OCR 결과 인라인"""
    _, upload_col, _ = st.columns([0.5, 3, 0.5])
    with upload_col:
        st.markdown("<div style='text-align:center; font-size:14px; color:#555;'>거래처 명함 업로드</div>",
                    unsafe_allow_html=True)
        fu_col, btn_col = st.columns([3, 1])
        with fu_col:
            uploaded = st.file_uploader(
                "파일 선택", type=["png", "jpg", "jpeg", "pdf"],
                key="card_uploader", label_visibility="collapsed",
            )
        with btn_col:
            st.markdown("")
            st.button("업로드", key="btn_card_upload", use_container_width=True)

        if not uploaded:
            return

        st.markdown("---")
        st.markdown("<div style='text-align:center; font-size:13px; color:#555;'>OCR기반 기업정보 확인</div>",
                    unsafe_allow_html=True)
        with st.container(border=True):
            if uploaded.type in ("image/png", "image/jpeg", "image/jpg"):
                st.image(uploaded, width=180)
            for k, v in MOCK_OCR.items():
                st.write(f"{k} : {v}")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ 정보 확인 완료", key="btn_ocr_ok", use_container_width=True):
                st.success("확인 완료. 아래 계약서 업로드 섹션으로 이동하세요.")
        with c2:
            if st.button("🔄 다시 업로드", key="btn_ocr_retry", use_container_width=True):
                st.rerun()


# ─────────────────────────────────────────────
# SECTION 2 — 계약서 업로드 및 표준 비교
# ─────────────────────────────────────────────
def section_contract():
    st.markdown('<a name="sec-contract"></a>', unsafe_allow_html=True)
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # 검토요청 생성 팝업 (현장 의견 통합)
    if st.session_state["show_review_modal"]:
        _review_modal()
        return

    with st.container(border=True):
        st.markdown("**계약서 업로드 및 표준 비교**")
        col_cfg, col_up = st.columns([1, 1])

        with col_cfg:
            st.markdown("계약 구분:")
            contract_type = st.radio(
                "계약 구분", ["기본 계약", "개별 계약"],
                horizontal=True, label_visibility="collapsed",
                key="r_contract_type", index=1,
            )
            st.markdown("표준 여부:")
            st.radio(
                "표준 여부", ["표준", "비표준"],
                horizontal=True, label_visibility="collapsed", key="r_standard_yn",
            )

        with col_up:
            st.markdown("**계약서 PDF 드래그/클릭 업로드**")
            st.caption("지원 형식: Textable PDF / 스캔본은 추출 실패 처리")
            pdf = st.file_uploader(
                "계약서 PDF", type=["pdf"],
                key="contract_pdf", label_visibility="collapsed",
            )
            if pdf:
                st.session_state["contract_uploaded"] = True
                st.session_state["contract_filename"] = pdf.name
                st.session_state["contract_type"] = contract_type

    if not st.session_state["contract_uploaded"]:
        st.info("계약서 PDF를 업로드하면 분석 결과가 표시됩니다.")
        return

    st.markdown("")

    # 분석 결과 배지 + 파일 정보
    col_badges, col_file = st.columns(2)
    with col_badges:
        for label, val in [("리스크 톤", "Med"), ("비표준 조항", "5건"), ("표준 유사", "82%")]:
            with st.container(border=True):
                st.markdown(f"#### {label} &nbsp; `{val}`")

    with col_file:
        for label, val in [
            ("파일명",    st.session_state["contract_filename"]),
            ("페이지 수", "200"),
            ("추출상태",  "완료"),
            ("분석유형",  "표준 유사형"),
        ]:
            with st.container(border=True):
                st.markdown(f"**{label} : {val}**")

    st.markdown("")

    # 검토요청 생성 버튼
    _, mid_col, _ = st.columns([1, 2, 1])
    with mid_col:
        if st.button("검토요청 생성", key="btn_open_review", use_container_width=True):
            st.session_state["show_review_modal"] = True
            st.rerun()

    if st.session_state.get("review_id"):
        st.success(
            f"검토요청 생성 완료 — 요청ID: **{st.session_state['review_id']}** | "
            f"중요도: {st.session_state.get('review_priority','High')} | 상태: 법무 검토 대기"
        )




def _review_modal():
    """검토요청 생성 팝업 — 중요도 + 현장 의견 통합"""
    st.markdown("")
    with st.container(border=True):
        _, title_col, _ = st.columns([0.5, 3, 0.5])
        with title_col:
            st.markdown(
                "<div style='text-align:center; font-size:20px; font-weight:700; "
                "border:1px solid #ccc; border-radius:8px; padding:10px; margin-bottom:16px;'>"
                "검토요청 생성</div>",
                unsafe_allow_html=True,
            )

        st.markdown("중요도")
        priority = st.selectbox(
            "중요도",
            ["High", "Medium", "Low"],
            index=["High", "Medium", "Low"].index(
                st.session_state.get("review_priority", "High")
            ),
            label_visibility="collapsed",
            key="sel_priority",
        )

        st.markdown("")
        st.markdown("**현장 의견**")
        with st.container(border=True):
            comment = st.text_area(
                "현장 의견",
                value=st.session_state.get("review_comment", ""),
                height=150,
                placeholder=(
                    "예)\n"
                    "- 해당 조항은 기존 거래에서도 사용된 조항입니다.\n"
                    "- 리스크 낮음\n"
                    "- 법무 검토 요청"
                ),
                label_visibility="collapsed",
            )
            op_col, _ = st.columns([1, 3])
            with op_col:
                if st.button("의견 전송", key="btn_opinion_send", use_container_width=True):
                    st.session_state["field_opinion"] = comment
                    st.success("의견이 저장되었습니다.")

        st.markdown("")
        _, done_col, _ = st.columns([1, 2, 1])
        with done_col:
            if st.button("생성 완료", key="btn_review_done", use_container_width=True):
                st.session_state["review_priority"] = priority
                st.session_state["review_comment"] = comment
                st.session_state["field_opinion"] = comment
                st.session_state["review_id"] = "REQ-2024-0392"
                st.session_state["show_review_modal"] = False
                st.rerun()

        _, cancel_col, _ = st.columns([2, 1, 2])
        with cancel_col:
            if st.button("취소", key="btn_review_cancel", use_container_width=True):
                st.session_state["show_review_modal"] = False
                st.rerun()


# ─────────────────────────────────────────────
# SECTION 3 — AI 리스크 검토
# ─────────────────────────────────────────────
def section_ai_risk():
    st.markdown('<a name="sec-ai"></a>', unsafe_allow_html=True)
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    if not st.session_state.get("contract_uploaded"):
        st.info("먼저 위 계약서 업로드 섹션에서 계약서를 업로드해 주세요. (아래는 Mock 결과)")

    col_left, col_right = st.columns([1, 1.9])

    with col_left:
        with st.container(border=True):
            st.markdown(
                "<div style='text-align:center; font-size:18px; font-weight:700; "
                "border:1px solid #ccc; border-radius:8px; padding:12px; margin-bottom:16px;'>"
                "AI리스크 검토</div>",
                unsafe_allow_html=True,
            )
            st.markdown("<div style='text-align:center; color:#777; font-size:13px;'>계약정보</div>",
                        unsafe_allow_html=True)
            st.markdown("")
            with st.container(border=True):
                st.write(f"계약 유형 : {st.session_state.get('contract_type', '기본 계약')}")
                st.write("분석 상태 : 완료")
                st.write(f"AI 분석 결과 : 리스크 **{len(MOCK_RISKS)}건** 발견")

    with col_right:
        with st.container(border=True):
            _, head_col, _ = st.columns([0.5, 3, 0.5])
            with head_col:
                st.markdown(
                    "<div style='text-align:center; font-size:16px; font-weight:700; "
                    "border:1px solid #ccc; border-radius:8px; padding:8px; margin-bottom:12px;'>"
                    "AI 리스크 분석 결과</div>",
                    unsafe_allow_html=True,
                )

            st.info("ℹ️ AI가 분석한 결과를 바탕으로 실무자가 최종 검토를 진행해야 합니다. "
                    "위험 요소(리스크) 항목을 꼼꼼히 확인해 주세요.")

            st.markdown(
                f"🛡 **AI 리스크 분석 상세** &nbsp;"
                f"<span style='background:#fce8e6; color:#c5221f; padding:2px 10px; "
                f"border-radius:12px; font-size:12px; font-weight:700;'>총 {len(MOCK_RISKS)}건</span>",
                unsafe_allow_html=True,
            )
            st.caption("계약서 내에서 발견된 잠재적 위험 요소입니다.")
            st.markdown("")

            # 리스크 카드 — 모두 펼쳐서 표시 (expander 없음)
            for risk in MOCK_RISKS:
                with st.container(border=True):
                    st.markdown(
                        f"<span class='risk-no'>{risk['no']}</span> **{risk['title']}**",
                        unsafe_allow_html=True,
                    )
                    for b in risk["bullets"]:
                        st.markdown(f"&nbsp;&nbsp;&nbsp;{b}")

                    # 원문 보기 토글
                    btn_key = f"btn_raw_{risk['no']}"
                    if st.button("원문 보기", key=btn_key):
                        hl  = f"show_hl_{risk['no']}"
                        src = f"show_src_{risk['no']}"
                        toggled = not st.session_state.get(hl, False)
                        st.session_state[hl]  = toggled
                        st.session_state[src] = toggled

                    if st.session_state.get(f"show_hl_{risk['no']}"):
                        st.info(f"📌 **하이라이트**\n\n{risk['highlight']}")
                    if st.session_state.get(f"show_src_{risk['no']}"):
                        st.warning(f"📄 **출처**\n\n{risk['source']}")


# ─────────────────────────────────────────────
# SECTION 4 — 실무 Q&A
# ─────────────────────────────────────────────
def section_qna():
    st.markdown('<a name="sec-qna"></a>', unsafe_allow_html=True)
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # 근거 출처 팝업
    if st.session_state.get("show_source_modal") and st.session_state.get("source_modal_key"):
        _source_modal(st.session_state["source_modal_key"])

    st.markdown("**실무 Q&A (더미 RAG)**")
    st.write("답변은 데모용 더미응답이며, 근거 출처 링크를 함께 제공합니다.")

    # FAQ 칩 버튼
    chip_cols = st.columns(3)
    for i, chip in enumerate(FAQ_CHIPS):
        with chip_cols[i % 3]:
            if st.button(chip, key=f"chip_{i}", use_container_width=True):
                src_key = "SRC-107" if "선지급" in chip else ("SRC-042" if "리스크" in chip else None)
                st.session_state["qna_history"].append(
                    {"role": "user", "content": chip, "src": None}
                )
                st.session_state["qna_history"].append({
                    "role": "assistant",
                    "content": FAQ_ANSWERS.get(chip, "해당 질문에 대한 더미 답변입니다."),
                    "src": src_key,
                })
                st.rerun()

    st.markdown("")

    # 대화 창
    with st.container(border=True):
        if not st.session_state["qna_history"]:
            st.markdown("")
            st.caption("Q: xxxxx")
            st.caption("A: xxxx")
            st.markdown("")
        else:
            for idx, msg in enumerate(st.session_state["qna_history"]):
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])
                    if msg.get("src"):
                        src_key = msg["src"]
                        st.markdown(
                            f'<span class="src-tag">{src_key}</span>',
                            unsafe_allow_html=True,
                        )
                        if st.button(
                            f"근거 확인 ({src_key})",
                            key=f"btn_src_{idx}",
                        ):
                            st.session_state["show_source_modal"] = True
                            st.session_state["source_modal_key"] = src_key
                            st.rerun()

    # 입력창 — text_input + 버튼으로 고정 (chat_input은 floating이라 제거)
    with st.container(border=True):
        inp_col, send_col = st.columns([5, 1])
        with inp_col:
            user_input = st.text_input(
                "질문 입력",
                placeholder="질문 입력 : 예) 기본계약이 없으면 어떻게 진행하나요?",
                label_visibility="collapsed",
                key="qna_text_input",
            )
        with send_col:
            send_clicked = st.button("▶", key="btn_qna_send", use_container_width=True)

    if send_clicked and user_input.strip():
        st.session_state["qna_history"].append(
            {"role": "user", "content": user_input.strip(), "src": None}
        )
        st.session_state["qna_history"].append({
            "role": "assistant",
            "content": "현재 mock 모드입니다. 실제 서비스에서는 내부 지식 베이스(RAG)를 기반으로 AI가 답변합니다.",
            "src": None,
        })
        st.rerun()

    if st.session_state["qna_history"]:
        if st.button("대화 초기화", key="btn_clear_qna"):
            st.session_state["qna_history"] = []
            st.rerun()


def _source_modal(src_key: str):
    """근거 출처 팝업"""
    src = SOURCE_DB.get(src_key, {})
    with st.container(border=True):
        col_t, col_c = st.columns([9, 1])
        with col_t:
            st.markdown("#### 근거 출처")
        with col_c:
            if st.button("닫기", key="btn_src_close"):
                st.session_state["show_source_modal"] = False
                st.session_state["source_modal_key"] = ""
                st.rerun()

        # 태그
        tags_html = "".join(
            f'<span class="src-tag" style="margin-right:6px; '
            f'background:{"#e8f5e9" if i==0 else "#e3f2fd"}; '
            f'border-color:{"#4caf50" if i==0 else "#2196f3"}; '
            f'color:{"#2e7d32" if i==0 else "#1565c0"};">{t}</span>'
            for i, t in enumerate(src.get("tags", []))
        )
        st.markdown(tags_html, unsafe_allow_html=True)
        st.markdown("")

        col_a, col_b = st.columns(2)
        with col_a:
            with st.container(border=True):
                st.caption("문서명")
                st.markdown(f"**{src.get('문서명', '-')}**")
        with col_b:
            with st.container(border=True):
                st.caption("조항")
                st.markdown(f"**{src.get('조항', '-')}**")

        with st.container(border=True):
            st.write(src.get("내용", "-"))


# ─────────────────────────────────────────────
# 메인
# ─────────────────────────────────────────────
def render_page():
    apply_wireframe_theme()
    page_header(PAGE_TITLE, "", badge="현장 검토")
    _nav()
    section_company()
    section_contract()
    section_ai_risk()
    section_qna()


render_page()