# add header to shop_info.txt
echo shop_id,city_name,location_id,per_pay,score,comment_cnt,shop_level,cate_1_name,cate_2_name,cate_3_name > show_info_header.txt
cat shop_info.txt >> shop_info_header.txt
mv shop_info_header.txt > shop_info.txt

# add header to user_view.txt
echo user_id,shop_id,time_stamp > user_view_header.txt
cat user_view.txt >> user_view_header.txt
mv user_view_header.txt > user_view.txt

# add header to user_pay.txt
echo user_id,shop_id,time_stamp > user_pay_header.txt
cat user_pay.txt >> user_pay_header.txt
mv user_pay_header.txt > user_pay.txt
