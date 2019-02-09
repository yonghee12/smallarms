from werkzeug.utils import secure_filename

filename = secure_filename("[QP] 현대카드_리워드광고 Daily Report_190207.xlsx")
# filename = "rw_report.xlsx"

# for name in filename.split("_"):
#     if name[-5:] == ".xlsx":
#         print(name[:-5])
print