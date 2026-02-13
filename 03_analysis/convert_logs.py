import os
import pandas as pd
import cfusdlog  # 같은 폴더에 cfusdlog.py가 있어야 합니다.

def convert_bin_to_csv():
    # 1. 경로 설정
    raw_data_path = r'F:\flapper\06_data\01_raw_logs'
    processed_data_path = r'F:\flapper\06_data\02_processed'
    
    # 출력 폴더가 없으면 생성
    if not os.path.exists(processed_data_path):
        os.makedirs(processed_data_path)
        print(f"폴더 생성 완료: {processed_data_path}")

    # 2. 변환할 파일 범위 설정 (100 ~ 104)
    log_prefix = "0206t"
    file_range = range(100, 105)

    print("변환 작업을 시작합니다...")
    print("-" * 40)

    for i in file_range:
        log_id = f"{log_prefix}{i}"
        input_file = os.path.join(raw_data_path, log_id)
        
        # 파일 존재 여부 확인
        if not os.path.exists(input_file):
            print(f"경고: 파일을 찾을 수 없습니다 -> {input_file}")
            continue

        try:
            # 3. 바이너리 데이터 디코딩
            logData = cfusdlog.decode(input_file)
            
            # 'fixedFrequency' 데이터 유무 확인
            if 'fixedFrequency' in logData:
                df = pd.DataFrame(logData['fixedFrequency'])
                
                # 4. CSV 파일로 저장
                output_filename = f"{log_id}.csv"
                output_path = os.path.join(processed_data_path, output_filename)
                
                df.to_csv(output_path, index=False)
                print(f"성공: {log_id} -> {output_filename}")
            else:
                print(f"알림: {log_id}에 'fixedFrequency' 데이터가 없습니다.")
                
        except Exception as e:
            print(f"에러: {log_id} 변환 중 오류 발생 -> {e}")

    print("-" * 40)
    print("모든 작업이 완료되었습니다.")

if __name__ == "__main__":
    convert_bin_to_csv()