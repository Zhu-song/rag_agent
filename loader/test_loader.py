# -*- coding: utf-8 -*-
# 测试所有文档加载器是否正常工作

import sys
import os

# 导入你的4个加载器
from pdf_loader import load_pdf
from doc_loader import load_docx
from text_loader import load_txt
from url_loader import load_url

# ====================== 测试开始 ======================
if __name__ == "__main__":
    print("=" * 60)
    print("🧪 文档加载器 综合测试")
    print("=" * 60)

    # 1. 测试 TXT
    print("\n📄 测试 TXT 加载器：")
    try:
        test_txt = "test.txt"
        with open(test_txt, "w", encoding="utf-8") as f:
            f.write("这是测试文本\nHello World")
        txt_content = load_txt(test_txt)
        print("✅ 成功：", txt_content[:20])
        os.remove(test_txt)
    except Exception as e:
        print("❌ 失败：", e)

    # 2. 测试 PDF
    print("\n📕 测试 PDF 加载器：")
    try:
        pdf_text = load_pdf("test.pdf")  # 换成你自己的PDF路径
        print("✅ PDF 内容长度：", len(pdf_text))
    except Exception as e:
        print("ℹ️ 未找到测试PDF，跳过：", e)

    # 3. 测试 DOCX
    print("\n📗 测试 DOCX 加载器：")
    try:
        doc_text = load_docx("test.docx")  # 换成你自己的Word路径
        print("✅ Word 内容长度：", len(doc_text))
    except Exception as e:
        print("ℹ️ 未找到测试Word，跳过：", e)

    # 4. 测试 URL
    print("\n🌍 测试 URL 网页加载器：")
    try:
        url_text = load_url("https://www.baidu.com")
        print("✅ 网页内容长度：", len(url_text))
    except Exception as e:
        print("❌ 失败：", e)

    print("\n" + "=" * 60)
    print("🎉 全部测试完成！你的环境已经正常！")
    print("=" * 60)