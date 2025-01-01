import os

def combine_merblogs():
    try:
        print("파일 통합 시작...")
        
        # 현재 디렉토리와 MerBlogs 폴더 경로 설정
        current_dir = os.path.dirname(os.path.abspath(__file__))
        merblogs_dir = os.path.join(current_dir, 'MerBlogs')
        output_file = os.path.join(current_dir, 'MerBlogs.txt')
        
        # MerBlogs 폴더의 모든 파일 목록 가져오기
        files = os.listdir(merblogs_dir)
        print(f"총 {len(files)}개의 파일을 찾았습니다.")
        
        # 통합 파일 생성
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for i, filename in enumerate(files, 1):
                file_path = os.path.join(merblogs_dir, filename)
                print(f"[{i}/{len(files)}] 처리 중: {filename}")
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                        outfile.write(content)
                        outfile.write('\n\n')
                        outfile.write('-' * 100)
                        outfile.write('\n\n')
                except Exception as e:
                    print(f"파일 처리 중 오류 발생: {filename}")
                    print(f"오류 내용: {str(e)}")
                    continue
        
        print(f"\n모든 파일이 '{output_file}'로 통합되었습니다.")
        
    except Exception as e:
        print(f"프로그램 실행 중 오류 발생: {str(e)}")

if __name__ == "__main__":
    combine_merblogs()
