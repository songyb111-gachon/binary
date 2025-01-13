import re
import tkinter as tk
from tkinter import filedialog


def extract_psnr_step_524288(file_path):
    results = []

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        # 각 데이터셋의 Step: 524288의 정보를 추출하는 정규식
        matches = re.finditer(
            r"Starting pixel flip optimization for file (\d+\.png) with initial PSNR: .*?"
            r"Step: 524288\s+"
            r"PSNR Before: (\d+\.\d+)\s+\|\s+PSNR After: (\d+\.\d+)\s+\|.*?"
            r"Diff: (\d+\.\d+).*?"
            r"Optimization completed\. Final PSNR improvement: (\d+\.\d+)",
            content,
            re.DOTALL,
        )
        for match in matches:
            file_name = match.group(1)  # 파일 이름 (예: 1.png)
            psnr_after = match.group(3)  # Step: 524288의 PSNR After 값
            psnr_improvement = match.group(5)  # 최종 PSNR 개선값

            # 파일 이름을 '001.png', '002.png' 형식으로 변경
            formatted_file_name = f"{int(file_name.split('.')[0]):04}.png"

            # 결과 추가
            #results.append(
            #    f"{formatted_file_name} Optimization completed. Final PSNR improvement: {psnr_improvement}. PSNR After: {psnr_after}"
            #)
            # 결과 추가
            results.append(
                f"{formatted_file_name} | PSNR Diff: {psnr_improvement} | PSNR After: {psnr_after}"
            )
    return results


def open_file_and_extract():
    # 파일 선택 GUI 열기
    file_path = filedialog.askopenfilename(
        title="Select Log File",
        filetypes=[("Log Files", "*.log"), ("All Files", "*.*")]
    )
    if not file_path:
        print("No file selected.")
        return

    # PSNR 데이터 추출
    results = extract_psnr_step_524288(file_path)

    # 결과 GUI 창에 표시
    result_window = tk.Toplevel()
    result_window.title("PSNR Results")
    text_widget = tk.Text(result_window, wrap="word", width=80, height=20)
    text_widget.pack(expand=True, fill="both")
    text_widget.insert("1.0", "\n".join(results))

    # 결과 저장 옵션
    output_file = filedialog.asksaveasfilename(
        title="Save Results As",
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            for result in results:
                f.write(result + "\n")
        print(f"Results saved to {output_file}")


# GUI 설정
root = tk.Tk()
root.title("Log File PSNR Extractor")

# 버튼 추가
select_button = tk.Button(root, text="Select Log File", command=open_file_and_extract, width=30)
select_button.pack(pady=20)

# 메인 루프 실행
root.mainloop()
