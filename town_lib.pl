########################################################
#クッキーネームの変更
$COOKIE_NAME = 'town_maker2';
# 多重登録許可の名前 ('許可名前１','許可名前２','3');と続きます。
@tazyu_kyoka = ();
# 行動時間制限個別設定
%work_seigen = ();
# 行動待機時間
%seigen = ();
# 特殊の家使いナンバー(0から始まる)
$tokusyu_ie_no = '';
#特定の街を隠す 'yes'
$machikakushi = 'no';
#隠す街の番号
$kakushimachi_no = '';
$kakushimachi_no1 = '';
$kakushimachi_no2 = '';
$kakushimachi_no3 = '';
$kakushimachi_no4 = '';
#隠す街の名前
$kakushimachi_name = '';
$kakushimachi_name1 = '';
$kakushimachi_name2 = '';
$kakushimachi_name3 = '';
$kakushimachi_name4 = '';
# 音を出すか(yes,no)
$otdashi = 'yes';
# 掲示板へのタグ書き込みを無効にする。(yes,no)
$kigiban_tag = 'yes';
# eval{ flock (OUT, 2); }を使う。
$eval_flock = 'no';
# イベント記録ファイル名
$event_fail = "./log_dir/event_kanri.cgi";
# 優遇時間 3秒
$yuguujikan = 3;
########################################################

####################################################
#/////////////////以下サブルーチン/////////////////#
####################################################

#アタッカー対策
sub atakka {
	my $get_host = $ENV{'REMOTE_HOST'};
	my $get_addr = $ENV{'REMOTE_ADDR'};
	if ($get_host eq "" || $get_host eq $get_addr) {
		$get_host = gethostbyaddr(pack("C4", split(/\./, $get_addr)), 2) || $get_addr;
	}
	$c_tim = time;
	
	open(AT,"< atakka.cgi") || error("Open error attaka.cgi");
	eval{ flock (AT, 1); };
	@tem_atakku = <AT>;
	close(AT);
	$i=0;
	$ma_aru =0;
	@new_tem_atakku = ();
	foreach (@tem_atakku){
		($ma_addr,$ma_host,$ma_tim,$ma_kaisu) = split(/<>/);
		if($ma_addr eq $get_addr && $get_host eq $ma_host){
			$ma_aru =1;
			if($ma_kaisu > 9){
				error("あなたの更新回数が非常に多いので攻撃者とみなされました。");
			}else{
				$ma_kaisu++;
				unshift @new_tem_atakku,"$get_addr<>$get_host<>$c_tim<>$ma_kaisu<>\n";
				next;
			}
		}
		if($ma_kaisu > 9){
			unshift @new_tem_atakku,$_;
			next;
		}
		if($ma_tim + 3 < $c_tim){
			next;
		}
		unshift @new_tem_atakku,$_;
	}
	if(!$ma_aru){
		unshift @new_tem_atakku,"$get_addr<>$get_host<>$c_tim<>1<>\n";
	}
	open(AT,"> atakka.cgi") || error("Write error attaka.cgi");
	eval{ flock (AT, 2); };
	print AT @new_tem_atakku;
	close(AT);
} #end

#---------------中のスタイルシート-------------------#
sub town_stylesheet{
	if($in{'size'}){$fontsize=$in{'size'};}
	if($fontsize ne "10" and $fontsize ne "11" and $fontsize ne "12" and $fontsize ne "13" and $fontsize ne "14" and $fontsize ne "15" and $fontsize ne "16"){$fontsize=13;}
	
	print <<"EOM";
<style type="text/css">
<!--
.dai {  font-size: $fontsize\px; font-weight: bold;color: #000000}	/*大きな文字*/
.tyuu {  font-size: $fontsize\px; color: #ff6600}	/*ステータス中見出し*/
.honbun2 {  font-size: $fontsize\px; line-height: 16px; color: #006699}	/*ステータス項目部分*/
.honbun3 {  font-size: $fontsize\px; line-height: 13px; color: #006699}	/*パラメータ項目部分*/
.honbun5 {  font-size: $fontsize\px; line-height: 13px; color: #339900}	/*キャラのパラメータ項目部分*/
.honbun4 {  font-size: $fontsize\px; line-height: 22px; color: #006699}	/*中くらいの文字*/
.job_messe {  font-size: $fontsize\px; line-height: 22px; color: #000000}	/*パラメータメッセージ*/
.small {  font-size: $fontsize\px; color: #444444}	/*小さい文字*/
.midasi {  font-size: 16px; font-weight: bold; text-align: center;color: #666666}	/*街の名前*/
.gym_style { background-color:#ffcc33; background-image:url($img_dir/shop_bak.gif)}	/*ジムの背景*/
.syokudou_style { background-color:#ccff66; background-image:url($img_dir/shop_bak.gif)}	/*食堂の背景*/
.orosi_style { background-color:#996633; background-image:url($img_dir/shop_bak.gif)}	/*卸問屋の背景*/
.job_style { background-color:#669966; background-image:url($img_dir/shop_bak.gif)}	/*ハローワークの背景*/
.school_style { background-color:#339999; background-image:url($img_dir/shop_bak.gif)}	/*学校の背景*/
.ginkou_style { background-color:#999999; background-image:url($img_dir/shop_bak.gif)}	/*銀行の背景*/
.yakuba_style { background-color:#336699; background-image:url($img_dir/shop_bak.gif)}	/*役場の背景*/
.item_style { background-color:#ffcc66; background-image:url($img_dir/command_bak.gif)}	/*アイテム使用画面の背景*/
.kentiku_style { background-color:#996666; background-image:url($img_dir/command_bak.gif)}	/*建築会社の背景*/
.omise_list_style { background-color:#b293ad; background-image:url($img_dir/shop_bak.gif)}	/*個人お店の商品リスト背景*/
.prof_style { background-color:#ccff99; background-image:url($img_dir/shop_bak.gif)}	/*プロフィール画面背景*/
.keiba_style { background-color:#99cc66; }	/*競馬背景*/

.yosumi {  border: #666666; border-style: solid; border-top-width: 1px; border-right-width: 1px; border-bottom-width: 1px; border-left-width: 1px; background-color:#ffffff}	/*街ステータス窓*/

.sumi {  border: #000000; border-style: solid; border-top-width: 0px; border-right-width: 1px; border-bottom-width: 1px; border-left-width: 0px}
.migi {  border: #000000; border-style: solid; border-top-width: 0px; border-right-width: 0px; border-bottom-width: 0px; border-left-width: 0px}
.sita {  border: #000000; border-style: solid; border-top-width: 0px; border-right-width: 0px; border-bottom-width: 0px; border-left-width: 0px}
.sita2 {  border: #666666; border-style: solid; border-top-width: 0px; border-right-width: 0px; border-bottom-width: 1px; border-left-width: 0px}
.jouge {  border: #000000; border-style: solid; border-top-width: 1px; border-right-width: 0px; border-bottom-width: 1px; border-left-width: 0px}
.message {  font-size: $fontsize\px; line-height: 16px; color: #000000;}

.purasu {color: #009900;}
.mainasu { color: #ff3300;}
.kuro {  font-size: $fontsize\px; text-align: left;color: #000000}
.honbun {  font-size: $fontsize\px; line-height: 16px; color: #000000}
.loto {  font-size: 28px; color: #000000;line-height:180%;}
.naka {  border: #000000; border-style: solid; border-top-width: 1px; border-right-width: 0px; border-bottom-width: 1px; border-left-width: 0px}

a{text-decoration:none;}
a:link {color:#0000FF;}
a:visited {color:#0000FF;}
a:hover {color:#FF0000;}
a:active {color:#FF0000;}
body {font-size:$fontsize\px;color:#000000 }
table {font-size:$fontsize\px;color:#000000;}
-->
</style>
EOM
}

#---------------独自タグ-------------------#
sub tag{
	my($tag)=@_[0];
	until ($tag eq $tag2) {
		$tag2=$tag;
		$tag =~ s/\[sun\]/<img src="img\/mini\/ic_sun.gif">/g;
		$tag =~ s/\[sun\]/<img src="img\/mini\/ic_sun.gif">/g;
		$tag =~ s/\[cloudy\]/<img src="img\/mini\/ic_cloudy.gif">/g;
		$tag =~ s/\[typhoon\]/<img src="img\/mini\/ic_typhoon.gif">/g;
		$tag =~ s/\[rain\]/<img src="img\/mini\/ic_rain.gif">/g;
		$tag =~ s/\[thunder\]/<img src="img\/mini\/ic_thunder.gif">/g;
		$tag =~ s/\[snow\]/<img src="img\/mini\/ic_snow.gif">/g;
		$tag =~ s/\[smoking\]/<img src="img\/mini\/ic_smoking.gif">/g;
		$tag =~ s/\[ribbon\]/<img src="img\/mini\/ic_ribbon.gif">/g;
		$tag =~ s/\[fog\]/<img src="img\/mini\/ic_fog.gif">/g;
		$tag =~ s/\[gemini\]/<img src="img\/mini\/ic_gemini.gif">/g;
		$tag =~ s/\[spit\]/<img src="img\/mini\/ic_spit.gif">/g;
		$tag =~ s/\[taurus\]/<img src="img\/mini\/ic_taurus.gif">/g;
		$tag =~ s/\[aries\]/<img src="img\/mini\/ic_aries.gif">/g;
		$tag =~ s/([^=^\"]|^)(\[)(b+)(,)([^\]]*)(\])/$1<b>$5<\/b>/g;
		$tag =~ s/([^=^\"]|^)(\[)(i+)(,)([^\]]*)(\])/$1<i>$5<\/i>/g;
		$tag =~ s/([^=^\"]|^)(\[)(u+)(,)([^\]]*)(\])/$1<u>$5<\/u>/g;
		$tag =~ s/([^=^\"]|^)(\[)(s+)(,)([^\]]*)(\])/$1<s>$5<\/s>/g;
		$tag =~ s/([^=^\"]|^)(\[)(color:red+)(,)([^\]]*)(\])/$1<font color="red">$5<\/font>/g;
		$tag =~ s/([^=^\"]|^)(\[)(color:blue+)(,)([^\]]*)(\])/$1<font color="blue">$5<\/font>/g;
		$tag =~ s/([^=^\"]|^)(\[)(color:green+)(,)([^\]]*)(\])/$1<font color="green">$5<\/font>/g;
		$tag =~ s/([^=^\"]|^)(\[)(color:yellow+)(,)([^\]]*)(\])/$1<font color="yellow">$5<\/font>/g;
		$tag =~ s/([^=^\"]|^)(\[)(bg:red+)(,)([^\]]*)(\])/$1<span style="background-color:red;">$5<\/span>/g;
		$tag =~ s/([^=^\"]|^)(\[)(bg:blue+)(,)([^\]]*)(\])/$1<span style="background-color:blue;">$5<\/span>/g;
		$tag =~ s/([^=^\"]|^)(\[)(bg:green+)(,)([^\]]*)(\])/$1<span style="background-color:green;">$5<\/span>/g;
		$tag =~ s/([^=^\"]|^)(\[)(bg:yellow+)(,)([^\]]*)(\])/$1<span style="background-color:yellow;">$5<\/span>/g;
		$tag =~ s/([^=^\"]|^)(\[)(https?\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#\%]+)(,)([^\]]*)(\])/$1<a href=\"$3\" target=\"_blank\">$5<\/a>/g;
	}
	$tag =~ s/(&gt;&gt;)(\d+)/<a href\="\#$2"><b><font color\=\#ff00ff>>>$2<\/font><\/b><\/a>/g;
	$tag =~ s/([^=^\"]|^)(https?\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#\%]+)/$1<a href=\"$2\" target=\"_blank\">$2<\/a>/g;
	$tag =~ s/(&gt;)(\d+)/<font color=\"\#999999\">$2<\/font>/g;
	return $tag;
}

#---------------個人ログファイル分割-------------------#
sub kozin_sprit{
($k_id,$name,$pass,$money,$bank,$job,$kokugo,$suugaku,$rika,$syakai,$eigo,$ongaku,$bijutu,$looks,$tairyoku,$kenkou,$speed,$power,$wanryoku,$kyakuryoku,$love,$unique,$etti,$first_access,$kounyuu,$sex,$access_byou,$access_time,$host,$house_name,$house_type,$byoumei,$mise_type,$last_mailcheck,$super_teiki,$energy,$last_ene_time,$next_tra,$last_syokuzi_split,$sintyou,$taijuu,$nou_energy,$last_nouene_time,$job_keiken,$job_kaisuu,$last_school,$byouki_sisuu,$loan_nitigaku,$loan_kaisuu,$k_sousisan,$jobsyu,$k_yobi3,$kpoint,$idou_jikan,$brauza,$shiharai,$syoukai_id,$aki,$oto,$hatugen,$fontsize,$buki_name,$buki,$bougu_name,$bougu,$mahou_name,$mahou,$omamori_name,$omamori)= split(/<>/);
#k_yobi3＝多重登録者　　jobsyu＝マスターした職業　　kounyuu＝アイコンURL　house_name＝最後に仕事した時間　　house_type＝配偶者のID番号
#mise_type＝ログイン非表示　　last_mailcheck＝未使用　　$brauza 追加　　$shiharai=銀行の支払い形式
($last_syokuzi,$syo_sake,$syo_dezato,$syo_dorinku)=split(/=/, $last_syokuzi_split);
chomp $brauza;
chomp $shiharai;
chomp $syoukai_id;
chomp $aki;
chomp $oto;
chomp $hatugen;
chomp $fontsize;
chomp $buki_name;
chomp $buki;
chomp $bougu_name;
chomp $bougu;
chomp $mahou_name;
chomp $mahou;
chomp $omamori_name;
chomp $omamori;
}

#---------------個人ログファイル分割２-------------------#
sub kozin_sprit2 {
($k_id,$name,$pass,$money,$bank,$job,$kokugo,$suugaku,$rika,$syakai,$eigo,$ongaku,$bijutu,$looks,$tairyoku,$kenkou,$speed,$power,$wanryoku,$kyakuryoku,$love,$unique,$etti,$first_access,$kounyuu,$sex,$access_byou,$access_time,$host,$house_name,$house_type,$byoumei,$mise_type,$last_mailcheck,$super_teiki,$energy,$last_ene_time,$next_tra,$last_syokuzi_split,$sintyou,$taijuu,$nou_energy,$last_nouene_time,$job_keiken,$job_kaisuu,$last_school,$byouki_sisuu,$loan_nitigaku,$loan_kaisuu,$k_sousisan,$jobsyu,$k_yobi3,$kpoint,$idou_jikan,$brauza,$shiharai,$syoukai_id,$aki,$oto,$hatugen,$fontsize,$buki_name,$buki,$bougu_name,$bougu,$mahou_name,$mahou,$omamori_name,$omamori)= split(/<>/,@_[0]);
@nouryoku_suuzi_hairetu =  split(/<>/,@_[0]);
chomp $nouryoku_suuzi_hairetu[54];
chomp $nouryoku_suuzi_hairetu[55];
chomp $nouryoku_suuzi_hairetu[56];
chomp $nouryoku_suuzi_hairetu[57];
chomp $nouryoku_suuzi_hairetu[58];
chomp $nouryoku_suuzi_hairetu[59];
chomp $nouryoku_suuzi_hairetu[60];
chomp $nouryoku_suuzi_hairetu[61];
chomp $nouryoku_suuzi_hairetu[62];
chomp $nouryoku_suuzi_hairetu[63];
chomp $nouryoku_suuzi_hairetu[64];
chomp $nouryoku_suuzi_hairetu[65];
chomp $nouryoku_suuzi_hairetu[66];
chomp $nouryoku_suuzi_hairetu[67];
($last_syokuzi,$syo_sake,$syo_dezato,$syo_dorinku)=split(/=/, $last_syokuzi_split);
chomp $brauza;
chomp $shiharai;
chomp $syoukai_id;
chomp $aki;
chomp $oto;
chomp $hatugen;
chomp $fontsize;
chomp $buki_name;
chomp $buki;
chomp $bougu_name;
chomp $bougu;
chomp $mahou_name;
chomp $mahou;
chomp $omamori_name;
chomp $omamori;
}

#---------------自分のログファイル作成-------------------#
sub temp_routin {
	if ($money =~ /\D\-/){$money = 0;$bank = 0;}#破産プログラム指数（e+)になったら注意。
	$last_syokuzi_split = "$last_syokuzi=$syo_sake=$syo_dezato=$syo_dorinku";
	$k_temp="$k_id<>$name<>$pass<>$money<>$bank<>$job<>$kokugo<>$suugaku<>$rika<>$syakai<>$eigo<>$ongaku<>$bijutu<>$looks<>$tairyoku<>$kenkou<>$speed<>$power<>$wanryoku<>$kyakuryoku<>$love<>$unique<>$etti<>$first_access<>$kounyuu<>$sex<>$access_byou<>$access_time<>$host<>$house_name<>$house_type<>$byoumei<>$mise_type<>$last_mailcheck<>$super_teiki<>$energy<>$last_ene_time<>$next_tra<>$last_syokuzi_split<>$sintyou<>$taijuu<>$nou_energy<>$last_nouene_time<>$job_keiken<>$job_kaisuu<>$last_school<>$byouki_sisuu<>$loan_nitigaku<>$loan_kaisuu<>$k_sousisan<>$jobsyu<>$k_yobi3<>$kpoint<>$idou_jikan<>$brauza<>$shiharai<>$syoukai_id<>$aki<>$oto<>$hatugen<>$fontsize<>$buki_name<>$buki<>$bougu_name<>$bougu<>$mahou_name<>$mahou<>$omamori_name<>$omamori<>\n";
}

#---------------相手ログファイル分割-------------------#
sub aite_sprit {
($aite_k_id,$aite_name,$aite_pass,$aite_money,$aite_bank,$aite_job,$aite_kokugo,$aite_suugaku,$aite_rika,$aite_syakai,$aite_eigo,$aite_ongaku,$aite_bijutu,$aite_looks,$aite_tairyoku,$aite_kenkou,$aite_speed,$aite_power,$aite_wanryoku,$aite_kyakuryoku,$aite_love,$aite_unique,$aite_etti,$aite_first_access,$aite_kounyuu,$aite_sex,$aite_access_byou,$aite_access_time,$aite_host,$aite_house_name,$aite_house_type,$aite_byoumei,$aite_mise_type,$aite_last_mailcheck,$aite_super_teiki,$aite_energy,$aite_last_ene_time,$aite_next_tra,$aite_last_syokuzi,$aite_sintyou,$aite_taijuu,$aite_nou_energy,$aite_last_nouene_time,$aite_job_keiken,$aite_job_kaisuu,$aite_last_school,$aite_byouki_sisuu,$aite_loan_nitigaku,$aite_loan_kaisuu,$aite_sousisan,$aite_jobsyu,$aite_yobi3,$aite_kpoint,$aite_idou_jikan,$aite_brauza,$aite_shiharai,$aite_syoukai_id,$aite_aki,$aite_oto,$aite_hatugen,$aite_fontsize,$aite_buki_name,$aite_buki,$aite_bougu_name,$aite_bougu,$aite_mahou_name,$aite_mahou,$aite_omamori_name,$aite_omamori)= split(/<>/,@_[0]);
@aite_nouryoku_suuzi_hairetu =  split(/<>/,@_[0]);
#aite_yobi3＝多重登録
chomp $aite_brauza;
chomp $aite_shiharai;
chomp $aite_syoukai_id;
chomp $aite_aki;
chomp $aite_oto;
chomp $aite_hatugen;
chomp $aite_fontsize;
chomp $aite_buki_name;
chomp $aite_buki;
chomp $aite_bougu_name;
chomp $aite_bougu;
chomp $aite_mahou_name;
chomp $aite_mahou;
chomp $aite_omamori_name;
chomp $aite_omamori;
}

#---------------相手のログファイル作成-------------------#
sub aite_temp_routin {
	$aite_k_temp="$aite_k_id<>$aite_name<>$aite_pass<>$aite_money<>$aite_bank<>$aite_job<>$aite_kokugo<>$aite_suugaku<>$aite_rika<>$aite_syakai<>$aite_eigo<>$aite_ongaku<>$aite_bijutu<>$aite_looks<>$aite_tairyoku<>$aite_kenkou<>$aite_speed<>$aite_power<>$aite_wanryoku<>$aite_kyakuryoku<>$aite_love<>$aite_unique<>$aite_etti<>$aite_first_access<>$aite_kounyuu<>$aite_sex<>$aite_access_byou<>$aite_access_time<>$aite_host<>$aite_house_name<>$aite_house_type<>$aite_byoumei<>$aite_mise_type<>$aite_last_mailcheck<>$aite_super_teiki<>$aite_energy<>$aite_last_ene_time<>$aite_next_tra<>$aite_last_syokuzi<>$aite_sintyou<>$aite_taijuu<>$aite_nou_energy<>$aite_last_nouene_time<>$aite_job_keiken<>$aite_job_kaisuu<>$aite_last_school<>$aite_byouki_sisuu<>$aite_loan_nitigaku<>$aite_loan_kaisuu<>$aite_sousisan<>$aite_jobsyu<>$aite_yobi3<>$aite_kpoint<>$aite_idou_jikan<>$aite_brauza<>$aite_shiharai<>$aite_syoukai_id<>$aite_aki<>$aite_oto<>$aite_hatugen<>$aite_fontsize<>$aite_buki_name<>$aite_buki<>$aite_bougu_name<>$aite_bougu<>$aite_mahou_name<>$aite_mahou<>$aite_omamori_name<>$aite_omamori<>\n";
	@aite_k_temp = ();
	push (@aite_k_temp,$aite_k_temp);
}

#---------------登録者リストファイル分割-------------------#
sub list_sprit{
($list_k_id,$list_name,$list_pass,$list_money,$list_bank,$list_job,$list_kokugo,$list_suugaku,$list_rika,$list_syakai,$list_eigo,$list_ongaku,$list_bijutu,$list_looks,$list_tairyoku,$list_kenkou,$list_speed,$list_power,$list_wanryoku,$list_kyakuryoku,$list_love,$list_unique,$list_etti,$list_first_access,$list_kounyuu,$list_sex,$list_access_byou,$list_access_time,$list_host,$list_house_name,$list_house_type,$list_byoumei,$list_mise_type,$list_last_mailcheck,$list_super_teiki,$list_energy,$list_last_ene_time,$list_next_tra,$list_last_syokuzi,$list_sintyou,$list_taijuu,$list_nou_energy,$list_last_nouene_time,$list_job_keiken,$list_job_kaisuu,$list_last_school,$list_byouki_sisuu,$list_loan_nitigaku,$list_loan_kaisuu,$list_sousisan,$list_jobsyu,$list_k_yobi3,$list_kpoint,$list_idou_jikan,$list_k_brauza,$list_k_shiharai,$list_syoukai_id,$list_aki,$list_oto,$list_hatugen,$list_fontsize,$list_buki_name,$list_buki,$list_bougu_name,$list_bougu,$list_mahou_name,$list_mahou,$list_omamori_name,$list_omamori)= split(/<>/,@_[0]);
chomp $list_k_brauza;
chomp $list_k_shiharai;
chomp $list_syoukai_id;
chomp $list_aki;
chomp $list_oto; 
chomp $list_hatugen;
chomp $list_fontsize;
chomp $list_buki_name;
chomp $list_buki;
chomp $list_bougu_name;
chomp $list_bougu;
chomp $list_mahou_name;
chomp $list_mahou;
chomp $list_omamori_name;
chomp $list_omamori;
}

#---------------登録者リストファイル作成-------------------#
sub list_temp {
	$list_temp="$list_k_id<>$list_name<>$list_pass<>$list_money<>$list_bank<>$list_job<>$list_kokugo<>$list_suugaku<>$list_rika<>$list_syakai<>$list_eigo<>$list_ongaku<>$list_bijutu<>$list_looks<>$list_tairyoku<>$list_kenkou<>$list_speed<>$list_power<>$list_wanryoku<>$list_kyakuryoku<>$list_love<>$list_unique<>$list_etti<>$list_first_access<>$list_kounyuu<>$list_sex<>$list_access_byou<>$list_access_time<>$list_host<>$list_house_name<>$list_house_type<>$list_byoumei<>$list_mise_type<>$list_last_mailcheck<>$list_super_teiki<>$list_energy<>$list_last_ene_time<>$list_next_tra<>$list_last_syokuzi<>$list_sintyou<>$list_taijuu<>$list_nou_energy<>$list_last_nouene_time<>$list_job_keiken<>$list_job_kaisuu<>$list_last_school<>$list_byouki_sisuu<>$list_loan_nitigaku<>$list_loan_kaisuu<>$list_sousisan<>$list_jobsyu<>$list_k_yobi3<>$list_kpoint<>$list_idou_jikan<>$list_k_brauza<>$list_k_shiharai<>$list_syoukai_id<>$list_aki<>$list_oto<>$list_hatugen<>$list_fontsize<>$list_buki_name<>$list_buki<>$list_bougu_name<>$list_bougu<>$list_mahou_name<>$list_mahou<>$list_omamori_name<>$list_omamori<>\n";
}

#---------------メイン街の分割-------------------#
sub main_town_sprit{
($mt_zinkou,$mt_keizai,$mt_hanei,$mt_today,$mt_orosiflag,$mt_t_time,$mt_y_time,$mt_syokudouflag,$mt_departflag,$total_ninzuu,$mt_yobi8,$mt_yobi9,$mt_yobi10,$mt_yobi11,$mt_yobi12,$mt_yobi13,$mt_yobi14)= split(/<>/,@_[0]);
#mt_yobi8 = 創設日（お店の売り上げまたは掲示板書き込みがあった日）　　mt_yobi9＝卸更新日時　　total_ninzuu＝未使用
}

#---------------メイン街のファイル作成-------------------#
sub main_town_temp{
	$mt_temp="$mt_zinkou<>$mt_keizai<>$mt_hanei<>$mt_today<>$mt_orosiflag<>$mt_t_time<>$mt_y_time<>$mt_syokudouflag<>$mt_departflag<>$total_ninzuu<>$mt_yobi8<>$mt_yobi9<>$mt_yobi10<>$mt_yobi11<>$mt_yobi12<>$mt_yobi13<>$mt_yobi14<>\n";
	@mt_temp = ();
	push (@mt_temp,$mt_temp);
}

#---------------街のアイコンファイル分割-------------------#
sub town_sprit{
($town_name,$zinkou,$keizai,$hanei,$t_x0,$t_x1,$t_x2,$t_x3,$t_x4,$t_x5,$t_x6,$t_x7,$t_x8,$t_x9,$t_x10,$t_x11,$t_x12,$t_x13,$t_x14,$t_x15,$t_x16,$t_a0,$t_a1,$t_a2,$t_a3,$t_a4,$t_a5,$t_a6,$t_a7,$t_a8,$t_a9,$t_a10,$t_a11,$t_a12,$t_a13,$t_a14,$t_a15,$t_a16,$t_b0,$t_b1,$t_b2,$t_b3,$t_b4,$t_b5,$t_b6,$t_b7,$t_b8,$t_b9,$t_b10,$t_b11,$t_b12,$t_b13,$t_b14,$t_b15,$t_b16,$t_c0,$t_c1,$t_c2,$t_c3,$t_c4,$t_c5,$t_c6,$t_c7,$t_c8,$t_c9,$t_c10,$t_c11,$t_c12,$t_c13,$t_c14,$t_c15,$t_c16,$t_d0,$t_d1,$t_d2,$t_d3,$t_d4,$t_d5,$t_d6,$t_d7,$t_d8,$t_d9,$t_d10,$t_d11,$t_d12,$t_d13,$t_d14,$t_d15,$t_d16,$t_e0,$t_e1,$t_e2,$t_e3,$t_e4,$t_e5,$t_e6,$t_e7,$t_e8,$t_e9,$t_e10,$t_e11,$t_e12,$t_e13,$t_e14,$t_e15,$t_e16,$t_f0,$t_f1,$t_f2,$t_f3,$t_f4,$t_f5,$t_f6,$t_f7,$t_f8,$t_f9,$t_f10,$t_f11,$t_f12,$t_f13,$t_f14,$t_f15,$t_f16,$t_g0,$t_g1,$t_g2,$t_g3,$t_g4,$t_g5,$t_g6,$t_g7,$t_g8,$t_g9,$t_g10,$t_g11,$t_g12,$t_g13,$t_g14,$t_g15,$t_g16,$t_h0,$t_h1,$t_h2,$t_h3,$t_h4,$t_h5,$t_h6,$t_h7,$t_h8,$t_h9,$t_h10,$t_h11,$t_h12,$t_h13,$t_h14,$t_h15,$t_h16,$t_i0,$t_i1,$t_i2,$t_i3,$t_i4,$t_i5,$t_i6,$t_i7,$t_i8,$t_i9,$t_i10,$t_i11,$t_i12,$t_i13,$t_i14,$t_i15,$t_i16,$t_j0,$t_j1,$t_j2,$t_j3,$t_j4,$t_j5,$t_j6,$t_j7,$t_j8,$t_j9,$t_j10,$t_j11,$t_j12,$t_j13,$t_j14,$t_j15,$t_j16,$t_k0,$t_k1,$t_k2,$t_k3,$t_k4,$t_k5,$t_k6,$t_k7,$t_k8,$t_k9,$t_k10,$t_k11,$t_k12,$t_k13,$t_k14,$t_k15,$t_k16,$t_l0,$t_l1,$t_l2,$t_l3,$t_l4,$t_l5,$t_l6,$t_l7,$t_l8,$t_l9,$t_l10,$t_l11,$t_l12,$t_l13,$t_l14,$t_l15,$t_l16,$t_m0,$t_m1,$t_m2,$t_m3,$t_m4,$t_m5,$t_m6,$t_m7,$t_m8,$t_m9,$t_m10,$t_m11,$t_m12,$t_m13,$t_m14,$t_m15,$t_m16,$t_n0,$t_n1,$t_n2,$t_n3,$t_n4,$t_n5,$t_n6,$t_n7,$t_n8,$t_n9,$t_n10,$t_n11,$t_n12,$t_n13,$t_n14,$t_n15,$t_n16,$tika,$t_yobi2,$t_yobi3,$t_yobi4,$t_yobi5,$t_yobi6,$t_yobi7)= split(/<>/,@_[0]);
@town_sprit_matrix =  split(/<>/,@_[0]);
#t_yobi2 = 街設立日（その街の売り上げがあった日）
}

#---------------仕事ファイル分割-------------------#
sub job_sprit {
($job_no,$job_name,$job_kokugo,$job_suugaku,$job_rika,$job_syakai,$job_eigo,$job_ongaku,$job_bijutu,$job_BMI_min,$job_BMI_max,$job_looks,$job_tairyoku,$job_kenkou,$job_speed,$job_power,$job_wanryoku,$job_kyakuryoku,$job_kyuuyo,$job_siharai,$job_love,$job_unique,$job_etti,$job_sex,$job_sintyou,$job_energy,$job_nou_energy,$job_rank,$job_syurui,$job_bonus,$job_syoukyuuritu)= split(/<>/,@_[0]);
}

#---------------商品ファイル分割-------------------#
sub syouhin_sprit{
($syo_syubetu,$syo_hinmoku,$syo_kokugo,$syo_suugaku,$syo_rika,$syo_syakai,$syo_eigo,$syo_ongaku,$syo_bijutu,$syo_kouka,$syo_looks,$syo_tairyoku,$syo_kenkou,$syo_speed,$syo_power,$syo_wanryoku,$syo_kyakuryoku,$syo_nedan,$syo_love,$syo_unique,$syo_etti,$syo_taikyuu,$syo_taikyuu_tani,$syo_kankaku,$syo_zaiko,$syo_cal,$syo_siyou_date,$syo_sintai_syouhi,$syo_zunou_syouhi,$syo_comment,$syo_kounyuubi,$tanka,$tokubai)= split(/<>/,@_[0]);
$syo_comment =~ s/</&lt;/g;
$syo_comment =~ s/>/&gt;/g;
}

#---------------商品ファイル作成-------------------#
sub syouhin_temp{
	$syo_temp="$syo_syubetu<>$syo_hinmoku<>$syo_kokugo<>$syo_suugaku<>$syo_rika<>$syo_syakai<>$syo_eigo<>$syo_ongaku<>$syo_bijutu<>$syo_kouka<>$syo_looks<>$syo_tairyoku<>$syo_kenkou<>$syo_speed<>$syo_power<>$syo_wanryoku<>$syo_kyakuryoku<>$syo_nedan<>$syo_love<>$syo_unique<>$syo_etti<>$syo_taikyuu<>$syo_taikyuu_tani<>$syo_kankaku<>$syo_zaiko<>$syo_cal<>$syo_siyou_date<>$syo_sintai_syouhi<>$syo_zunou_syouhi<>$syo_comment<>$syo_kounyuubi<>$tanka<>$tokubai<>\n";
}

#---------------ジムファイル分割-------------------#
sub gym_sprit{
($gym_name,$gym_looks,$gym_tairyoku,$gym_kenkou,$gym_speed,$gym_power,$gym_wanryoku,$gym_kyakuryoku,$gym_nedan,$gym_kouka,$gym_etti,$gym_kankaku,$gym_syouhi)= split(/<>/,@_[0]);
}

#---------------学校ファイル分割-------------------#
sub school_sprit{
($sc_name,$sc_kokugo,$sc_suugaku,$sc_rika,$sc_syakai,$sc_eigo,$sc_ongaku,$sc_bijutu,$sc_nedan,$sc_kouka,$sc_syouhi)= split(/<>/,@_[0]);
}

#---------------銀行明細ファイル分割-------------------#
sub ginkou_meisai_sprit {
($meisai_date,$meisai_naiyou,$meisai_hikidasi,$meisai_azuke,$meisai_zandaka,$meisai_syubetu)= split(/<>/,@_[0]);
}

#---------------家ファイル分割-------------------#
sub ori_ie_sprit {
($ori_k_id,$ori_ie_name,$ori_ie_setumei,$ori_ie_image,$ori_ie_syubetu,$ori_ie_kentikubi,$ori_ie_town,$ori_ie_tateziku,$ori_ie_yokoziku,$ori_ie_sentaku_point,$ori_ie_rank,$ori_ie_rank2,$ori_ie_yobi8,$ori_ie_yobi9,$ori_ie_jyouhou)= split(/<>/,@_[0]);
}

#---------------家ファイル作成-------------------#
sub ori_ie_temp {
$ori_ie_temp = "$ori_k_id<>$ori_ie_name<>$ori_ie_setumei<>$ori_ie_image<>$ori_ie_syubetu<>$ori_ie_kentikubi<>$ori_ie_town<>$ori_ie_tateziku<>$ori_ie_yokoziku<>$ori_ie_sentaku_point<>$ori_ie_rank<>$ori_ie_rank2<>$ori_ie_yobi8<>$ori_ie_yobi9<>$ori_ie_jyouhou<>\n";
}

#---------------家の設定ファイル分割-------------------#
sub oriie_settei_sprit {
($my_con1,$my_con2,$my_con3,$my_con4,$my_con1_title,$my_con2_title,$my_con3_title,$my_con4_title,$my_yobi5,$my_yobi6,$my_yobi7,$my_yobi8,$my_yobi9,$my_yobi10,$my_yobi11,$my_yobi12,$my_yobi13,$my_yobi14,$my_yobi15,$my_yobi16,$my_yobi17,$my_yobi18)= split(/<>/,@_[0]);
	@oriie_settei_sprit = split(/<>/,@_[0]);
}

#---------------家の設定ファイル作成-------------------#
sub oriie_settei_temp {
$ori_ie_settei_temp = "$my_con1<>$my_con2<>$my_con3<>$my_con4<>$my_con1_title<>$my_con2_title<>$my_con3_title<>$my_con4_title<>$my_yobi5<>$my_yobi6<>$my_yobi7<>$my_yobi8<>$my_yobi9<>$my_yobi10<>$my_yobi11<>$my_yobi12<>$my_yobi13<>$my_yobi14<>$my_yobi15<>$my_yobi16<>$my_yobi17<>$my_yobi18<>\n";
}

#---------------メールファイル分割-------------------#
sub  mail_sprit {
	($m_syubetu,$m_name,$m_com,$m_date,$m_byou,$m_yobi1,$m_yobi2,$m_yobi3,$m_yobi4,$m_yobi5)= split(/<>/,@_[0]);
}

#---------------ログ更新-------------------#
sub log_kousin {
		&lock;
		if (@_[1] ne ""){
			open(OUT,">@_[0]") || &error("@_[0]が開けません1");
			eval{ flock (OUT, 2); };
			print OUT @_[1];
			close(OUT);
			if (-z @_[0]){
				$loop_count = 0;
				while ($loop_count <= 10){
					for (0..50){$i=0;}
					if ($loop_count == 10){&error("ファイル@_[0]が消えています管理者に連絡ください。");}
					@f_stat_b = stat(@_[0]);
					$size_f = $f_stat_b[7];
					if ($size_f == 0 && @_[1] ne ""){
						open (DAT, "> @_[0] ") or &error("@_[0]が開けません2");
						eval{ flock (DAT, 2); };
						print DAT @_[1] ;
						close (DAT);
					}else{
						last;
					}
				$loop_count++;
				}
			}
		}
		&unlock;
}

#---------------自分のログファイル開く-------------------#
sub openMylog {
		$my_log_file = "./member/@_[0]/log.cgi";
		open(MYL,"< $my_log_file") || &error("ログファイル（$my_log_file）が開けません。<br>再度ログインしても同様ならば管理人（$master_ad）までメールをください。");
		eval{ flock (MYL, 1); };
		$my_prof = <MYL>;
		if($my_prof == ""){&error("ログファイルに問題が起こりました。<br>お手数ですが、管理人（$master_ad）までメールをください。");}
		&kozin_sprit2($my_prof);
		close(MYL);
}

#---------------相手のログファイル開く-------------------#
sub openAitelog {
	$aite_log_file = "./member/@_[0]/log.cgi";
	if (-e $aite_log_file){
		open(AIT,"< $aite_log_file") || &error("お相手の方のログファイル（$aite_log_file）が開けません。");
		eval{ flock (AIT, 1); };
		$aite_prof = <AIT>;
		if($aite_prof == ""){&error("@_[0]/log.cgi お相手の方のログファイルに問題があります。");}
		&aite_sprit($aite_prof);
		close(AIT);
	}
}

#---------------大阪のおばちゃんのログファイル開く-------------------#
sub obalog {
	$oba_log_file = "./member/osaka/@_[0]log.cgi";
	if (-e $w_oba_log_file){
		open(OB,"< $w_oba_log_file") || &error("お相手の方のログファイル（$w_oba_log_file）が開けません。");
		eval{ flock (OB, 1); };
		$aite_prof = <OB>;
		if($aite_prof == ""){&error("@_[0]/log.cgi お相手の方のログファイルに問題があります。");}
		&aite_sprit($aite_prof);
		close(OB);
	}
}

#---------------弱い大阪のおばちゃんのログファイル開く-------------------#
sub weekobalog {
	$w_oba_log_file = "./member/osaka/w@_[0]log.cgi";
	if (-e $w_oba_log_file){
		open(WOL,"< $w_oba_log_file") || &error("お相手の方のログファイル（$w_oba_log_file）が開けません。");
		eval{ flock (WOL, 1); };
		$aite_prof = <WOL>;
		if($aite_prof == ""){&error("w@_[0]/log.cgi お相手の方のログファイルに問題があります。");}
		&aite_sprit($aite_prof);
		close(WOL);
	}
}

#---------------強い大阪のおばちゃんのログファイル開く-------------------#
sub strongobalog {
	$s_oba_log_file = "./member/osaka/s@_[0]log.cgi";
	if (-e $s_oba_log_file){
		open(SOL,"< $s_oba_log_file") || &error("お相手の方のログファイル（$s_oba_log_file）が開けません。");
		eval{ flock (SOL, 1); };
		$aite_prof = <SOL>;
		if($aite_prof == ""){&error("s@_[0]/log.cgi お相手の方のログファイルに問題があります。");}
		&aite_sprit($aite_prof);
		close(SOL);
	}
}

#---------------パスワードチェック-------------------#
sub check_pass{
	if($in{'k_id'} eq ""){
		if($in{'name'} eq ""){&error("ログインしてください。");}
		&id_check($in{'name'});
		$k_id = $return_id;
	}else{
		$k_id = $in{'k_id'};
	}
	
	$my_log_file = "./member/$k_id/log.cgi";
	open(MYL,"< $my_log_file") || &error("ログファイル（$my_log_file）が開けません。<br>再度ログインしても同様ならば管理人（$master_ad）までメールをください。");
	eval{ flock (MYL, 1); };
	$my_prof = <MYL>;
	close(MYL);
	
	if($my_prof == ""){&error("ログファイルに問題が起こりました。<br>お手数ですが、管理人（$master_ad）までメールをください。");}
	&kozin_sprit2($my_prof);
	if($in{'pass'} ne $pass){
		&error("名前とパスワードが一致しません！");
	}
	if ($tajuukinsi_deny==1){
		if($k_yobi3 ne ""){
			&error("多重登録者は入居できません。<br>$k_yobi3");
		}
	}
	if ($in{'burauza_in'} ne "" and $in{'burauza_in'} ne $brauza){
		$brauza = $in{'burauza_in'};
	}
}

#---------------BMI算出-------------------#
sub check_BMI {
	if(@_[0] == 0){
		$BMI = 0;
		$taikei = "やせすぎ";
	}else{
		$BMI = int (@_[1] / (@_[0] / 100) / (@_[0] / 100) );
		if($BMI >= 26){$taikei = "肥満";}
		elsif($BMI >= 24){$taikei = "やや太り気味";}
		elsif($BMI >= 20){$taikei = "標準";}
		elsif($BMI >= 18){$taikei = "やせ気味";}
		elsif($BMI <= 17){$taikei = "やせすぎ";}
	}
}

#---------------ヘッダー出力-------------------#
sub header {
	$heder_flag=1;
	print "Content-type: text/html;\n";
#gzip対応
	if($ENV{'HTTP_ACCEPT_ENCODING'} =~ /gzip/ && $gzip ne ''){  
		if($ENV{'HTTP_ACCEPT_ENCODING'} =~ /x-gzip/){
			print "Content-encoding: x-gzip\n\n";
		}else{
			print "Content-encoding: gzip\n\n";
		}
			open(STDOUT,"| $gzip -1 -c");
		}else{
			print "\n";
		}
	print "<html>\n<head>\n<META http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\">\n";
	
	#=====街移動=====#
	if (($in{'command'} eq "mati_idou" || $in{'command'} eq "mati_idou2" || $in{'command'} eq "densya") && !$in{'name'}){&error("ログインしてください");}
	if ($in{'command'} eq "mati_idou" || $in{'command'} eq "mati_idou2"){
		if ($in{'maemati'} != 3){
			&motimono_kensa_ev('ローラースルーゴーゴー');
			if ($kensa_flag == 1){
				$maigo = 'yes';
			}else{
				if (int(rand(5)+1) == 1){
					$maigo = 'yes';
				}
			}
		}
		while(($syudan_name,$sokudo) = each %idou_syudan){
			push @syudan_names,$syudan_name;
			push @sokudos,$sokudo;
		}
		#+++++++++移動手段選択++++++++++
		$idousyudan = "徒歩で";
		$ziko_idousyudan = "徒歩";
		$matiidou_time2 = $matiidou_time;
		foreach (@syudan_names){
			&motimono_kensa("$_");
			if ($kensa_flag == 1){
				$idousyudan = "$_で";
				$ziko_idousyudan = "$_";
				$matiidou_time2 = $idou_syudan{$_};
				last;
			}
		}
		
		#+++++++++バスで移動++++++++++
		if ($in{'command'} eq "mati_idou2"){
			$maigo = 'no';
			$idousyudan = "バスで500円で";
			$ziko_idousyudan = "バス";
			$matiidou_time2 = 5;
			$money -= 500;
			
			&temp_routin;
			&log_kousin($my_log_file,$k_temp);
		}

		#+++++++++自転車、徒歩で移動++++++++++
		if ($ziko_idousyudan eq '徒歩' || $ziko_idousyudan eq '自転車'){
			if ($idou_jikan == 1){&error("移動中に更新しないでください。");}
			$idou_jikan = 1;
			$tairyku_up = int(rand(15)+1);
			$kenkou_up = int(rand(15)+1);
			$speed_up = int(rand(15)+1);
			$wanryoku_up = int(rand(15)+1);
			$kyakuryoku_up = int(rand(15)+1);
			if ($ziko_idousyudan eq '徒歩'){
				if ($tairyku_up <= 5){
					$tairyoku += $tairyku_up;
					$disp .= "体力が$tairyku_up　";
				}
				if ($kenkou_up <= 5){
					$kenkou += $kenkou_up;
					$disp .= "健康が$kenkou_up　";
				}
				if ($speed_up <= 5){
					$speed += $speed_up;
					$disp .= "スピードが$speed_up　";
				}
				if ($wanryoku_up <= 5){
					$wanryoku += $wanryoku_up;
					$disp .= "腕力が$wanryoku_up　";
				}
				if ($kyakuryoku_up <= 5){
					$kyakuryoku += $kyakuryoku_up;
					$disp .= "脚力が$kyakuryoku_up　";
				}
			}elsif($ziko_idousyudan eq '自転車'){
				if ($tairyku_up <= 3){
					$tairyoku += $tairyku_up;
					$disp .= "体力が$tairyku_up　";
				}
				if ($kenkou_up <= 3){
					$kenkou += $kenkou_up;
					$disp .= "健康が$kenkou_up　";
				}
				if ($speed_up <= 5){
					$speed += $speed_up;
					$disp .= "スピードが$speed_up　";
				}
				if ($wanryoku_up <= 5){
					$wanryoku += $wanryoku_up;
					$disp .= "腕力 $wanryoku_up　";
				}
				if ($kyakuryoku_up <= 5){
					$kyakuryoku += $kyakuryoku_up;
					$disp .= "脚力 $kyakuryoku_up　";
				}
			}
			&temp_routin;
			&log_kousin($my_log_file,$k_temp);
			if($disp){
				 $disp .= "きたえられた。";
			}
		}
		
		#+++++++++事故発生++++++++++
		$randed = int (rand($ziko_kakuritu)+1);
		if ($randed == 1 ){ $ziko_flag  = "on";}else{$ziko_flag  = "off";}
		if ($ziko_idousyudan eq 'バス'){$ziko_flag  = "off";}

		$idou_time = time + $matiidou_time2;
		
		#+++++++++街移動じゃないとき++++++++++
	}else{$idou_jikan = 0;}
	
	#=================仕事関連==========================
	if ($in{'mysec'}){
		if(abs($in{'mysec'} - $house_name) < 60*15){
			($sec_dis,$min_dis,$hour_dis,$mday_dis,$mon_dis,$year_dis,) = localtime($in{'mysec'} + 60*$work_seigen_time);
		}else{
			($sec_dis,$min_dis,$hour_dis,$mday_dis,$mon_dis,$year_dis,) = localtime($house_name + 60*$work_seigen_time);
		}
	}else{
		($sec_dis,$min_dis,$hour_dis,$mday_dis,$mon_dis,$year_dis,) = localtime($house_name + 60*$work_seigen_time);
	}
	$year_dis += 1900;
	$mon_dis++;
	if ($min_dis < 10){$min_dis = '0'.$min_dis}
	if ($sec_dis < 10){$sec_dis = '0'.$sec_dis}

	if ($brauza eq "Microsoft Internet Explorer" && $job ne "学生"){
		$disp_j1 = qq|document.getElementById('comm').innerHTML="<input type=image src=$img_dir/button/go_work.png onMouseOver=\\"Navi('$img_dir/button/go_work.png', '仕事', '仕事に出かけます。<br>経験値：$job_keiken　勤務数：$job_kaisuu回', 1, event);\\" onMouseOut=\\"NaviClose();\\">"|;
		$disp_j2 = qq|document.getElementById('comm').innerHTML="<input type=image src=$img_dir/button/no_work.png onMouseOver=\\"Navi('$img_dir/button/no_work.png', '仕事', '仕事に出かけられません。<br>経験値：$job_keiken　勤務数：$job_kaisuu回', 1, event);\\" onMouseOut=\\"NaviClose();\\">"|;
	}	
	#=================街移動、競馬==========================
	if ($in{'command'} eq "mati_idou" || $in{'command'} eq "mati_idou2" || $in{'command'} eq "densya"){
		$disp_in = <<"EOM";
		function idouInterval(){
			idou = setTimeout('idousuru()',$matiidou_time2*1000);	
		}
		function idousuru(){
			document.f_idou.submit();
		}
EOM
	}elsif ($in{'mode'} eq "keiba" && ($in{'command'} eq "start" || $in{'command'} eq "go")){
		$disp_in = <<"EOM";
		function umaInterval(){
			owari = document.keiba.count.value;
			if(owari == 0){
				idou = setTimeout('idousuru()',3*1000);
			}
		}
		function idousuru(){
			document.keiba.submit();
		}
EOM
	}
	
	print "<title>$subtitle</title>\n";

#=================トップ、建築のjavascript==========================
	if ($in{'mode'} eq '' || $in{'mode'} eq 'kentiku_do' || $in{'mode'} eq 'make_town'){
	print <<"EOM";
<SCRIPT type="text/javascript" language="JavaScript">
<!--
function Navi(img, title, title2, mode, event) {
	if(set.style.display == "block"){set.style.display = "none";}
	if(!event) var event=window.event;
	if(!event.pageX) event.pageX = event.clientX + document.body.scrollLeft;
	if(!event.pageY) event.pageY = event.clientY + document.body.scrollTop;
if(mode){
	set.style.left = event.pageX - 315;
}else{
	set.style.left = event.pageX + 15;
}
	set.style.top = event.pageY + 15;
	set.style.display = "block";
	document.getElementById('set').innerHTML="<table bgcolor='#eeeeee' border='3' bordercolor='#6464FF' cellspacing='0' cellpadding='3' width='300'><tr><td align='center'><img src=" + img + "></td><td><font size='2' color='#000000'><b>" + title + "</b></font><hr noshade size='2'><font size='2' color='#000000'>" + title2 + "</font></td></tr></table>";
	return false;
}
function NaviClose() {
set.style.display = "none";
}
//-->
</SCRIPT>
EOM

#=================競馬のjavascript==========================
	}elsif($in{'mode'} eq 'keiba'){
		print <<"EOM";
<SCRIPT type="text/javascript" language="JavaScript">
<!--
function imanotime(){
	if(document.ctw==null){clearInterval(retval_i);return;}
	if(document.ctw.mysec==null){clearInterval(retval_i);return;}
	mydate = new Date();
	document.ctw.mysec.value=Math.floor(mydate.getTime()/1000);
}
function pfvsetInterval(){
	retval_i = setInterval('imanotime()',1000);
}
$disp_in
// End -->
</Script>
EOM

#=================ログイン画面のjavascript==========================
	}elsif($in{'mode'} eq 'login_view'){
		if ($otdashi eq 'yes' && $brauza eq 'Microsoft Internet Explorer' && $oto eq 'on'){
			$oto1 = "		document.mymujic.Play();";
			$oto2 = "			document.mymujic.Stop();";
			$oto3 = "		document.mymujic.Stop();";
			$oto4 = "		document.mymujic2.Play();";
		}else{
			$oto1 = "//";
			$oto2 = "//";
			$oto3 = "//";
			$oto4 = "//";
		}

		print <<"EOM";
<SCRIPT type="text/javascript" language="JavaScript">
<!--
function Navi(img, title, title2, mode, event) {
	if(set.style.display == "block"){set.style.display = "none";}
	if(!event) var event=window.event;
	if(!event.pageX) event.pageX = event.clientX + document.body.scrollLeft;
	if(!event.pageY) event.pageY = event.clientY + document.body.scrollTop;
if(mode){
	set.style.left = event.pageX - 315;
}else{
	set.style.left = event.pageX + 15;
}
	set.style.top = event.pageY + 15;
	set.style.display = "block";
	document.getElementById('set').innerHTML="<table bgcolor='#eeeeee' border='3' bordercolor='#6464FF' cellspacing='0' cellpadding='3' width='300'><tr><td align='center'><img src=" + img + "></td><td><font size='2' color='#000000'><b>" + title + "</b></font><hr noshade size='2'><font size='2' color='#000000'>" + title2 + "</font></td></tr></table>";
	return false;
}
function NaviClose() {
set.style.display = "none";
}
//-->
</SCRIPT>
<Script Language="JavaScript">
<!--
///////////////////////////////////////////////////
// メッセージ No.5.1 Produced by「CLUB とむやん君」
// URL http://www2s.biglobe.ne.jp/~club_tom/
// 上の2行は著作権表示ですので消さないで下さい
///////////////////////////////////////////////////
function imanotime(){
	if(document.ctw==null){clearInterval(retval_i);return;}
	if(document.ctw.mysec==null){clearInterval(retval_i);return;}
	mydate = new Date();
	document.ctw.mysec.value=Math.floor(mydate.getTime()/1000);
}
function pfvsetInterval(){
	retval_w = setInterval('daytime()',1000);
	retval_i = setInterval('imanotime()',1000);
}
$disp_in
function daytime(){
	if(document.ct==null){clearInterval(retval_w);return;}
	if(document.ct.std==null){clearInterval(retval_w);return;}
	var d_t = document.ct.std.value;
	var space = " ";
	var dt = d_t.split(space);
	var dtime = new Date(dt[0],dt[1]-1,dt[2],dt[3],dt[4],dt[5]);
	var imat = new Date();

	nokorimd = (dtime.getTime() - imat.getTime() +1000)/(60*1000);
	if (nokorimd >= 0){
		nokorimd = Math.floor(nokorimd);
	}else{
		nokorimd = Math.ceil(nokorimd);
	}

	nokorim = (dtime.getTime() - imat.getTime())/(60*1000);
	if (nokorim >= 0){
		nokorim = Math.floor(nokorim);
	}else{
		nokorim = Math.ceil(nokorim);
	}
	nokoris = (dtime.getTime() - imat.getTime() - nokorim*60*1000)/1000;
	nokorihntei = nokoris;
	nokoris = Math.abs(nokoris);
	nokoris = Math.ceil(nokoris);
	if (nokorihntei >= 0){
		if(nokoris >= 60){nokoris = 0;}
		if(nokoris < 10){nokoris = "0" + nokoris;}
		document.getElementById("j_time").innerHTML = "仕事ができるまであと"+nokorimd +"分" + nokoris +"秒";
		$disp_j2;
	}else{
		document.getElementById("j_time").innerHTML = "仕事　ＯＫ";
$oto4		document.mymujic2.Play();
		clearInterval(retval_w);
		$disp_j1;
	}
}
// End -->
</Script>
EOM
	}

#=================ログイン、街移動、競馬、建築のBODY==========================
	&town_stylesheet;
	if ($in{'mode'} eq "login_view" || @_[1] eq "sonomati"){$sonomati_style_settei ="$page_back[$in{'town_no'}]";}

	if($in{'command'} eq "mati_idou" || $in{'command'} eq "mati_idou2" || $in{'command'} eq "densya"){
		print "</head><body style=\"$sonomati_style_settei\" class=@_[0] leftmargin=5 topmargin=5 marginwidth=5 marginheight=5 onLoad=\"idouInterval()\">\n";
	}elsif ($in{'mode'} eq "keiba" && ($in{'command'} eq "start" ||$in{'command'} eq "go")){
		print "</head><body style=\"$sonomati_style_settei\" class=@_[0] leftmargin=5 topmargin=5 marginwidth=5 marginheight=5 onLoad=\"umaInterval()\"><DIV ID=\"set\" style=\"position:absolute;display:none;z-index:10;\"></DIV>\n";
	}elsif($in{'mode'} eq "login_view"){
		print "</head><body style=\"$sonomati_style_settei\" class=@_[0] leftmargin=5 topmargin=5 marginwidth=5 marginheight=5 onLoad=\"pfvsetInterval()\"><DIV ID=\"set\" style=\"position:absolute;display:none;z-index:10;\"></DIV>\n";
		if ($otdashi eq 'yes'){
			if ($brauza ne "Microsoft Internet Explorer"){
				print "<EMBED src=\"./sd029.wav\" name=mymujic type=audio/wav autostart=\"false\" hidden=\"true\" loop=\"true\">\n";
				print "<EMBED src=\"./sd024.wav\" name=mymujic2 type=audio/wav autostart=\"false\" hidden=\"true\" loop=\"false\">\n";
			}else{
				print "<object name=\"mymujic\" classid=\"clsid:22D6F312-B0F6-11D0-94AB-0080C74C7E95\" width=\"0\" height=\"0\"><param name=\"SRC\" value=\"./sd029.wav\"><param name=\"AUTOSTART\" value=\"false\"><param name=\"loop\" value=\"true\">\n</object>\n";
				print "<object name=mymujic2 classid=\"clsid:22D6F312-B0F6-11D0-94AB-0080C74C7E95\" width=\"0\" height=\"0\"><param name=\"SRC\" value=\"./sd024.wav\"><param name=\"AUTOSTART\" value=\"false\"><param name=\"loop\" value=\"false\"></object>\n";
			}
		}
	}elsif ($in{'mode'} eq "make_town"){
		print "</head><body leftmargin=5 topmargin=5 marginwidth=5 marginheight=5><DIV ID=\"set\" style=\"position:absolute;display:none;z-index:10;\"></DIV>\n";
	}else {
		print "</head><body style=\"$sonomati_style_settei\" class=@_[0] leftmargin=5 topmargin=5 marginwidth=5 marginheight=5><DIV ID=\"set\" style=\"position:absolute;display:none;z-index:10;\"></DIV>\n";
	}
}

#---------------温泉とその他-------------------#
sub ori_header {
print "Content-type: text/html;\n";
		#+++++++++gzip対応++++++++++
		if($ENV{'HTTP_ACCEPT_ENCODING'} =~ /gzip/ && $gzip ne ''){  
		  if($ENV{'HTTP_ACCEPT_ENCODING'} =~ /x-gzip/){
			print "Content-encoding: x-gzip\n\n";
		  }else{
			print "Content-encoding: gzip\n\n";
		  }
		  open(STDOUT,"| $gzip -1 -c");
		}else{
		  print "\n";
		}
	print "<html>\n<head>\n<META http-equiv=\"content-type\" content=\"text/html;\">\n";
	print "<title>$subtitle</title>\n";

	if ($in{'mode'} eq 'onsen'){
		print <<"EOM";
<Script Language="JavaScript">
<!--
///////////////////////////////////////////////////
// メッセージ No.5.1 Produced by「CLUB とむやん君」
// URL http://www2s.biglobe.ne.jp/~club_tom/
///////////////////////////////////////////////////

// フォームにメッセージを書き込む部分です。
function powaInterval(){
	pwval = setInterval('powa_puro()',1000)
}
function powa_puro(){
	if(document.powa==null){clearInterval(pwval);return;}
	if(document.powa.ene==null || document.powa.nou==null){clearInterval(pwval);return;}

	var d_t_e = document.powa.ene.value;
	var d_t_n = document.powa.nou.value;
	var space = " ";
	var timup_e = 0;
	var timup_n = 0;
	var dt_e = d_t_e.split(space);
	var dt_n = d_t_n.split(space);
	var dtime_e = new Date(dt_e[0],dt_e[1]-1,dt_e[2],dt_e[3],dt_e[4],dt_e[5]);
	var dtime_n = new Date(dt_n[0],dt_n[1]-1,dt_n[2],dt_n[3],dt_n[4],dt_n[5]);
	var imat = new Date();

	nokorimd_e = (dtime_e.getTime() - imat.getTime() +1000)/(60*1000);
	if (nokorimd_e >= 0){
		nokorimd_e = Math.floor(nokorimd_e);
	}else{
		nokorimd_e = Math.ceil(nokorimd_e);
	}
	nokorim_e = (dtime_e.getTime() - imat.getTime())/(60*1000);
	if (nokorim_e >= 0){
		nokorim_e = Math.floor(nokorim_e);
	}else{
		nokorim_e = Math.ceil(nokorim_e);
	}
	nokoris_e = (dtime_e.getTime() - imat.getTime() - nokorim_e*60*1000)/1000;
	nokorihntei_e = nokoris_e
	nokoris_e = Math.abs(nokoris_e);
	nokoris_e = Math.ceil(nokoris_e);
	if (nokorihntei_e >= 0){
		if(nokoris_e >= 60){nokoris_e = 0;}
		if(nokoris_e < 10){nokoris_e = "0" + nokoris_e;}
		document.powa.tairyoku_pw.value = nokorimd_e +"分" + nokoris_e +"秒";
	}else{
		document.powa.tairyoku_pw.value = 'ＯＫ';
		timup_e = 1;
	}

	nokorimd_n = (dtime_n.getTime() - imat.getTime() +1000)/(60*1000);
	if (nokorimd_n >= 0){
		nokorimd_n = Math.floor(nokorimd_n);
	}else{
		nokorimd_n = Math.ceil(nokorimd_n);
	}

	nokorim_n = (dtime_n.getTime() - imat.getTime())/(60*1000);
	if (nokorim_n >= 0){
		nokorim_n = Math.floor(nokorim_n);
	}else{
		nokorim_n = Math.ceil(nokorim_n);
	}
	nokoris_n = (dtime_n.getTime() - imat.getTime() - nokorim_n*60*1000)/1000;
	nokorihntei_n = nokoris_n
	nokoris_n = Math.abs(nokoris_n);
	nokoris_n = Math.ceil(nokoris_n);
	if (nokorihntei_n >= 0){
		if(nokoris_n >= 60){nokoris_n = 0;}
		if(nokoris_n < 10){nokoris_n = "0" + nokoris_n;}
		document.powa.zunou_pw.value = nokorimd_n +"分" + nokoris_n +"秒";
	}else{
		document.powa.zunou_pw.value = 'ＯＫ';
		timup_n = 1;
	}

	if (timup_e == 1 && timup_n == 1){clearInterval(pwval);return;}

}
// End -->
</Script>
EOM
	}
	print <<"EOM";
<style type="text/css">
<!--
a	{@_[2]}
input  {@_[1]}
textarea {@_[1]}
select  {@_[1]}
body {@_[0]}
-->
</style>
EOM

	if ($in{'mode'} eq 'onsen'){
		print "</head><body leftmargin=5 topmargin=5 marginwidth=5 marginheight=5 onLoad=\"powaInterval()\"><DIV ID=\"set\" style=\"position:absolute;display:none;z-index:10;\"></DIV>\n";
	}else{
		print "</head><body leftmargin=5 topmargin=5 marginwidth=5 marginheight=5 $_[3]><DIV ID=\"set\" style=\"position:absolute;display:none;z-index:10;\"></DIV>\n";
	}
}

#---------------フッター-------------------#
sub hooter {
	if($in{'gamerand'}){
	print <<"EOM";
<div align=center><form method=POST action="gamerand.cgi">
<input type=hidden name=gamerand value="gamerand">
<!-- <input type=hidden name=mode value="donus"> -->
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=submit value="ゲームランドに戻る">
</form></div></body></html>
EOM
	exit;
	}

	if(@_[2]){$yobidasi_script = "@_[2]";}else{$yobidasi_script = "$script";}
	if ($yobidasi_script eq "admin.cgi"){
		$yobidasi_admin = "<input type=hidden name=kanrisya_id value=\"$kanrisya_id\"><input type=hidden name=admin_pass value=\"$admin_pass\">";
	}
	if(@_[1] ne ""){
	print <<"EOM";
	<div align=center><form method=POST action="$yobidasi_script">
	<input type=hidden name=mode value="@_[0]">
	<input type=hidden name=iesettei_id value="$in{'iesettei_id'}">
	$yobidasi_admin
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="@_[1]">
	</form></div>
EOM
	}
	if ($in{'mode'} eq "login_view" || $in{'mode'} eq ""){
		print <<"EOM";
<script language="JavaScript" type="text/javascript" src="http://axad.shinobi.jp/s/4ebd990d050e0b120b2b4a0da2e427ce/"></script>
<table width="100%" border="0"  cellspacing="0" cellpadding="2" style=" border: $st_win_wak; border-style: solid; border-width: 1px;" bgcolor=$st_win_back><tr><td align="center">
edit:たっちゃん｜<a href="../" target="_blank">HOMEへ</a>｜<a href="http://brassiere.jp/" target=_blank>- $version script by brassiere -</a></td></tr></table>
EOM
	}
	if (!$_[3]){
		print "</body></html>";
	}
	
}


#---------------メッセージ画面出力-------------------#
sub message {
&header("","sonomati");
#==========ロックフラグがあればロックディレクトリを削除=============
	if ($lockflag) { &unlock; }
	if(@_[2]){$yobidasi_script = "@_[2]";}else{$yobidasi_script = "$script";}
	if($ginkou_yobidasi){
	$kakikomi_1 = <<"EOM";
<form method=POST action="basic.cgi">
<input type=hidden name=mode value="ginkou">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$k_id">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=submit value="銀行へ"></form>
EOM
	}

	($in{'iesettei_id'},$bangou) = split(/_/,$in{'iesettei_id'});

	print <<"EOM";
<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>$_[0]</td></tr></table><br>
$kakikomi_1
<form method=POST action="$yobidasi_script">
<input type=hidden name=mode value="@_[1]">
<input type=hidden name=iesettei_id value="$in{'iesettei_id'}">
<input type=hidden name=kanrisya_id value="$in{'kanrisya_id'}">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=hidden name=admin_pass value="$in{'admin_pass'}">
<input type=submit value="戻る">
</form></div>
</body></html>
EOM
exit;
}

#---------------メッセージオンリー-------------------#
sub message_only {
	&header();
#==========ロックフラグがあればロックディレクトリを削除=============
	if ($lockflag) { &unlock; }
	print <<"EOM";
	<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>$_[0]</td></tr></table><br>
	</div>
EOM
}

#---------------エラー画面出力-------------------#
sub error {
if ($heder_flag ne "1"){
	&header("","sonomati");
}
	if ($_[1]){
		$botan = <<"EOM";
	<form method="POST" action="$script">
	<input type="hidden" name="mode" value="login_view">
	<input type="hidden" name="name" value="$in{'name'}">
	<input type="hidden" name="pass" value="$in{'pass'}">
	<input type="hidden" name="town_no" value="$in{'town_no'}">
	<input type="submit" value="戻る">
	</form>
EOM
	}
#==========ロックフラグがあればロックディレクトリを削除==========#
	if ($lockflag) { &unlock; }
	print <<"EOM";
	<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win">
	<tr><td>
	<center><h3><font color=#ff3300>ERROR !</font></h3>
	$_[0]
	<br><br><a href="javascript:history.back()"> [前の画面に戻る] </a>
	$botan
	</td></tr></table></div>
	<br>
EOM
	&hooter;

	exit;
}

#---------------ファイル読み込み-------------------#
sub readfile{
	open(IN,"< @_[0]") || &error("OPEN ERROR : @_[0]");
	eval{ flock (IN, 1); };
	return <IN>;
	close(IN);
}

#-----ファイル書き込み-----#
sub writefile{
	open(OUT,"> @_[0]") || &error("WRITE ERROR : @_[0]");
	eval{ flock (OUT, 2); };
	print OUT @_[1];
	close(OUT);
}

#---------------時間取得-------------------#
sub time_get {
	$date_sec = time ;
	local($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime($date_sec);
	@week = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
	$full_date = sprintf("%04d/%02d/%02d(%s) %02d:%02d:%02d",$year+1900,$mon+1,$mday,$week[$wday],$hour,$min,$sec);
	$date = sprintf("%04d/%02d/%02d",$year+1900,$mon+1,$mday);
	$date1 = sprintf("%04d/%02d/%02d %02d:%02d:%02d",$year+1900,$mon+1,$mday,$hour,$min,$sec);
	$date2 = sprintf("%04d/%02d/%02d %02d:%02d",$year+1900,$mon+1,$mday,$hour,$min);
	$date3 = sprintf("%02d/%02d %02d:%02d",$mon+1,$mday,$hour,$min);

	$return_hour=$hour;
}

#---------------time値（秒）を日付に変換-------------------#
sub byou_hiduke {
	$ENV{'TZ'} = "JST-9";
	my($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime(@_[0]);
	@week = ('日','月','火','水','木','金','土');
	$bh_full_date = sprintf("%02d月%02d日 %02d時%02d分",$mon+1,$mday,$hour,$min);
	$bh_date = sprintf("%04d/%02d/%02d",$year+1900,$mon+1,$mday);
	$bh_tukihi = sprintf("%02d/%02d",$mon+1,$mday);
	$bh_return_hour=$hour;
}

#---------------ホスト名を取得-------------------#
sub get_host {
	$return_host = $ENV{'REMOTE_HOST'};
	if (!$return_host){$return_host = $ENV{'REMOTE_ADDR'};}
	$addr = $ENV{'REMOTE_ADDR'};
	if ($return_host eq "" || $return_host eq $addr) {
		$return_host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2) || $addr;
	}
}

#---------------ロック処理-------------------#
sub lock {
	if($eval_flock eq 'yes'){return;}
	local($retry, $mtime);
#==========1分以上古いロックは削除する# 30sec 以上古いロックは削除=============
	if (-e $lockfile) {
		($mtime) = (stat($lockfile))[9];
		if ($mtime < time - 30) { &unlock; }
	}

#==========10回リトライ=============
	$retry = 20;
	while (!mkdir($lockfile, 0755)) {
		if (--$retry <= 0) { &error('ただいまサイトが混み合っています。少々お待ちください。'); }
		for (0..50){$i=0;}
	}
	$lockflag=1;
}


#---------------ロック解除-------------------#
sub unlock {
	if($eval_flock eq 'yes'){return;}
	#===== ロックディレクトリ削除 =====#
	rmdir($lockfile);
	#===== ロックフラグを解除 =====#
	$lockflag=0;
}

#---------------クッキーを取得-------------------#
sub get_cookie {
	my	($pair1, $cpair);
	foreach $pair1 (split(/;\s*/, $ENV{'HTTP_COOKIE'})) {
		my	($name1, $value1) = split(/=/, $pair1);
		
		#===== 単一のクッキー値から%COOKIEにデコード =====#
		if($name1 eq $COOKIE_NAME) {
			foreach $cpair (split(/&/, $value1)) {
				my	($cname, $cvalue) = split(/#/, $cpair);
				
				$cvalue =~ s/%([0-9a-fA-F][0-9a-fA-F])/chr(hex($1))/eg;
				$ck{$cname} = $cvalue;
			}
			last;
		}
	}
	
	if ($ck{'t_var'} ne "town2"){
		local($key, $val, @cook);
		@cook = split(/;/, $ENV{'HTTP_COOKIE'});
		foreach (@cook) {
			($key, $val) = split(/=/);
			$key =~ s/\s//g;
			$cook{$key} = $val;
		}
		%ck = split(/<>/, $cook{'town_maker'});
	}
	#===== 投稿直後にクッキー情報を表示 =====#
	if ($in{'name'}) { $ck{'name'} = $in{'name'}; }
	if ($in{'email'}) { $ck{'pass'} = $in{'pass'}; }
	if ($in{'hp'}) { $ck{'hp'} = $in{'hp'}; }
	if ($in{'town_no'}){$ck{'town_no'} = $in{'town_no'};}
}

#---------------クッキーを発行-------------------#
sub set_cookie {
	$ck{'name'} = $in{'name'};$ck{'pass'} = $in{'pass'};
	$ck{'hp'} = $in{'hp'};$ck{'t_var'} = "town2";
	$ck{'town_no'} = $in{'town_no'};

	$COOKIE_LIFE = 60;
	my	(@cpairs, $cname, $cvalue, $value1);
	
#==========%COOKIEを単一のクッキー値にエンコード=============
	foreach $cname (keys %ck) {
		$cvalue = $ck{$cname};
		$cvalue =~ s/(\W)/sprintf("%%%02X", ord $1)/eg;
		push @cpairs, "$cname#$cvalue";
	}
	$value1 = join('&', @cpairs);
	
#==========グリニッジ標準時の文字列=============
	my	@mon_str = qw(Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec);
	my	@wdy_str = qw(Sun Mon Tue Wed Thu Fri Sat);
	my	$life = $COOKIE_LIFE * 24 * 60 * 60;
	my	($sec, $min, $hour, $mday, $mon, $year, $wday) = gmtime(time + $life);
	my	$date0 = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",
			$wdy_str[$wday], $mday, $mon_str[$mon], $year + 1900, $hour, $min, $sec);
	print "Set-Cookie: $COOKIE_NAME=$value1; expires=$date0\n";
}

#---------------id番号獲得-------------------#
sub id_check{
	my($pass_id,$pass_name);
	open(IN,"< $pass_logfile") || &error("Open Error : $pass_logfile");
	eval{ flock (IN, 1); };
	$name_flag=0;
	while (<IN>) {
		($pass_id,$pass_name,$pass_pass)= split(/<>/);
		if($pass_name eq @_[0]){
			$name_flag=1;
			$return_id=$pass_id;
			last;
		}
	}
	close(IN);

	if(!$return_id){&error("IDが見つかりません。");}
	if($name_flag==0){
		$return_id="";
		&error("その名前では登録されてません");
	}
}

#---------------プロフィール削除-------------------#
sub prof_sakujo2 {
	open(PRO,"< $profile_file") || &error("Open Error : $profile_file");
	eval{ flock (PRO, 1); };
	my @pro_alldata=<PRO>;
	close(PRO);
	@new_pro_alldata = ();
	foreach (@pro_alldata){
		my ($pro_name,$pro_sex,$pro_age,$pro_addr,$pro_p1,$pro_p2,$pro_p3,$pro_p4,$pro_p5,$pro_p6,$pro_p7,$pro_p8,$pro_p9,$pro_p10,$pro_p11,$pro_p12,$pro_p13,$pro_p14,$pro_p15,$pro_p16,$pro_p17,$pro_p18,$pro_p19,$pro_p20)= split(/<>/);
		if (@_[0] eq "$pro_name"){next;} 
		push (@new_pro_alldata,$_);
	}
	
	#ログ更新
	open(PROO,">$profile_file") || &error("$profile_fileに書き込めません");
	eval{ flock (PROO, 2); };
	print PROO @new_pro_alldata;
	close(PROO);
}

#---------------斡旋所プロフィール削除-------------------#
sub as_prof_sakujo2 {
	open(ASP,"< $as_profile_file") || &error("Open Error : $as_profile_file");
	eval{ flock (ASP, 1); };
	my @as_pro_alldata=<ASP>;
	close(ASP);
	@as_new_pro_alldata = ();
	foreach (@as_pro_alldata){
		my ($pro_name,$pro_sex,$pro_age,$pro_addr,$pro_p1,$pro_p2,$pro_p3,$pro_p4,$pro_p5,$pro_p6,$pro_p7,$pro_p8,$pro_p9,$pro_p10,$pro_p11,$pro_p12,$pro_p13,$pro_p14,$pro_p15,$pro_p16,$pro_p17,$pro_p18,$pro_p19,$pro_p20)= split(/<>/);
		if (@_[0] eq "$pro_name"){next;} 
		push (@as_new_pro_alldata,$_);
	}
	
	#ログ更新
	open(ASPO,">$as_profile_file") || &error("$as_profile_fileに書き込めません");
	eval{ flock (ASPO, 2); };
	print ASPO @as_new_pro_alldata;
	close(ASPO);
}

#---------------削除の時結婚していたら、離婚をする。-------------------#
sub kekkon_sakujo {
	&id_check($_[0]);
	&openAitelog ($return_id);
	if ($aite_house_type eq ""){return;}
	$jibun_house_type = $aite_house_type;
	$aite_house_type = "";
	&aite_temp_routin;
	open(OUT,">$aite_log_file") || &error("$aite_log_fileが開けません");
	eval{ flock (OUT, 2); };
	print OUT $aite_k_temp;
	close(OUT);

	&openAitelog ($jibun_house_type);
	$aite_house_type = "";
	&aite_temp_routin;
	open(OUT,">$aite_log_file") || &error("$aite_log_fileが開けません");
	eval{ flock (OUT, 2); };
	print OUT $aite_k_temp;
	close(OUT);
}

#---------------アンケートの削除-------------------#
sub enq_sakujo_syori {
	open(IN,"< $enq_all") || &error("Open Error : $enq_all");
	eval{ flock (IN, 1); };
	@enq_list = <IN>;
	close(IN);
	
	@new_enq_list = ();
	foreach (@enq_list){
		chomp ($_);
		($enq_id,$enq_title,$enq_name,$enq_kazu,$enq_ninzuu,$enq_seigen,$enq_special)=split(/<>/);
		if($_[0] eq $enq_name){next;}
		push @new_enq_list,"$enq_id<>$enq_title<>$enq_name<>$enq_kazu<>$enq_ninzuu<>$enq_seigen<>$enq_special<>\n";
	}
	
	open(OIO,">$enq_all") || &error("$enq_allに書き込めません");
	eval{ flock (OIO, 2); };
	print OIO @new_enq_list;
	close(OIO);
}

#---------------家の削除-------------------#
sub ie_sakujo_syori {
#==========家リストへの書き込み=============
	open(IN,"< $ori_ie_list") || &error("Open Error : $ori_ie_list");
	eval{ flock (IN, 1); };
	@ori_ie_para = <IN>;
	close(IN);
	@new_ori_ie_list = ();
	foreach $tmp(@ori_ie_para){
		&ori_ie_sprit($tmp);
		if ($_[0] eq "$ori_ie_name"){
#==========タウン情報書き換え用に情報を取得=============
			$my_town_is = $ori_ie_town;
			$my_point_is = $ori_ie_sentaku_point;
#==========タウン情報に書き込み=============
			$write_town_data = "./log_dir/townlog". $my_town_is .".cgi";
			open(TWI,"< $write_town_data") || &error("Open Error : $write_town_data");
			eval{ flock (TWI, 1); };
			$hyouzi_town_hairetu = <TWI>;
			close(TWI);
			@town_sprit_matrix =  split(/<>/,$hyouzi_town_hairetu);
			($ori_ie_para_moto,$akichi) = split(/=/, $town_sprit_matrix[$my_point_is]);
			($ori_k_id_in,$syurui,$ori_k_no_in) = split(/_/, $ori_ie_para_moto);
			if (!$akichi){$akichi = "空地";}
			$town_sprit_matrix[$my_point_is] = "$akichi";
			$town_temp=join("<>",@town_sprit_matrix);
#==========タウン情報更新=============
			open(TWO,">$write_town_data") || &error("$write_town_dataに書き込めません");
			eval{ flock (TWO, 2); };
			print TWO $town_temp;
			close(TWO);

			next;
		}
		&ori_ie_temp;
		push (@new_ori_ie_list,$ori_ie_temp);
	}

#==========家リスト更新=============
		$i=0;
		$nijyuu = 0;
		foreach (@new_ori_ie_list){
			if ($_ eq $new_ori_ie_list[0] && $i){
				$nijyuu = $i;
				&error("二重書き込み t_l 1");
				last;
			}
			$i++;
		}
		if ($nijyuu){
			splice @new_ori_ie_list,$nijyuu;
		}
	open(OIO,">$ori_ie_list") || &error("$ori_ie_listに書き込めません");
	eval{ flock (OIO, 2); };
	print OIO @new_ori_ie_list;
	close(OIO);
}

#---------------デコード処理-------------------#
sub decode{
#&atakka; #koko2009/01/25
#===================メンテチェック================
if($mente_flag == 1){&error("$mente_message");}

#########１秒以内の更新禁止#########
#	open(IN,"< hostime.cgi") || &error("$write_town_dataに書き込めません");
#	eval{ flock (IN, 1); };
#	$hostime = <IN>;
#	close(IN);
#
#	chomp $hostime;
#	($mae_host,$mae_time)=split(/<>/,$hostime);
#	$now=time;
#
#	open(OUT,">hostime.cgi") || &error("$write_town_dataに書き込めません");
#	eval{ flock (OUT, 2); };
#	print OUT "$ENV{'REMOTE_ADDR'}<>$now<>";
#	close(OUT);
#	
#	if($mae_host eq $ENV{'REMOTE_ADDR'} and $now <= $mae_time + 1){&error("もうちょっと落ち着こうよ");}
####################################
	
	#=====変数の取得=====#
	local($buf, $key, $val, @buf, $cuntkey);
	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		$size = 5000;
		$remain = $ENV{'CONTENT_LENGTH'};
		if($remain > $size){&error("サイズオーバー");}
		read(STDIN, $query, $ENV{'CONTENT_LENGTH'});
	} else {
		$query = $ENV{'QUERY_STRING'};
	}
	
	#=====文字のデコード=====#
	foreach $pair (split(/&/, $query)) {
		($key, $value) = split(/=/, $pair);
		$value =~ tr/+/ /;
		$value =~ s/%([0-9a-fA-F][0-9a-fA-F])/chr(hex($1))/eg;

		if ($key eq 'loto' && $value ne ""){
			$loto6 .= "$value";
		}elsif(exists $in{$key}){
			$in{$key} = "$in{$key}<>$value";
		}else{
			$in{$key} = $value;
		}
	}
	
	while (($key,$value)=each %in){
		if ($key ne "upfile"){
			if ($key eq "m_com" || $key eq "b_com" || $key eq "a_com"){
				#$value =~ s/&/&amp;/g;
				$value =~ s/</&lt;/g;
				$value =~ s/>/&gt;/g;
				$value = &tag($value);
			}
			
			$value =~ s/document.cookie/どこみてんねん。クッキーうまー/g;
			$value =~ s/cookie/クッキーうま～/g;
			$value =~ s/\r\n/<br>/g;
			$value =~ s/\r/<br>/g;
			$value =~ s/\n/<br>/g;
			$value =~ s/<form/&lt;form/g;
			$value =~ s/<\/form>/&lt;\/form&gt;/g;
		}
		if($key ne 'loto'){
			$in{$key} = $value;
		}
		if($in{'my_data'}){
			($in{'name'},$in{'pass'},$in{'k_id'},$in{'town_no'},$in{'mode'})=split(/<>/,$in{'my_data'});
		}
		$value =~ s/<>/&lt;&gt;/g;
	}
	
	if ($in{'command'} eq "idousyuuryou"){
		if (time > $in{'idou'} + 5 || !$in{'idou'}){
			&error("エスパーブロック<br>ブラウザで戻ってください。");
		}
	}
	$in{'name'} =~ s/</&lt;/g;
	$in{'name'} =~ s/>/&gt;/g;
	$in{'pass'} =~ s/</&lt;/g;
	$in{'pass'} =~ s/>/&gt;/g;
	
	#=====不正アクセスの排除=====#
	if($in{'mode'} && $ENV{'HTTP_REFERER'}!~/http:\/\/w3.oroti.net\/~tyage\/town\//){
		&error("<a href='http://w3.oroti.net/~tyage/town/town_maker.cgi'>こちら</a>からお入りください。http://w3.oroti.net/~tyage/town/town_maker.cgi");
	}

	#=====禁止ホストの排除=====#
	$get_host = $ENV{'REMOTE_HOST'};
	$get_addr = $ENV{'REMOTE_ADDR'};
	if ($get_host eq "" || $get_host eq $get_addr) {
		$get_host = gethostbyaddr(pack("C4", split(/\./, $get_addr)), 2) || $get_addr;
	}
	if ($get_host eq "") { &error("恐れ入りますがホストが取得できない環境ではアクセスできません"); }

	open(IN,"< dene2.cgi") || &error("Open Error : dene2.cgi");
	eval{ flock (IN, 2); };
	@deny = <IN>;
	close(IN);

	foreach (@deny) {
		chomp $_;
		if($get_host =~ /$_/){&error("恐れ入りますがご利用中のホストからはアクセスできません");}
		if($get_addr =~ /$_/){&error("恐れ入りますがご利用中のホストからはアクセスできません");}
		if ($_ eq "") { next; }
		$_ =~ s/\*/\.\*/g;
		if ($get_host =~ /$_/i) { &error("恐れ入りますがご利用中のホストからはアクセスできません"); }
		if ($get_addr =~ /$_/i) { &error("恐れ入りますがご利用中のホストからはアクセスできません"); }
	}
	open(IN,"< dene2.cgi") || &error("Open Error : dene2.cgi");
	eval{ flock (IN, 2); };
	@deny = <IN>;
	close(IN);

	foreach (@deny) {
		chomp $_;
		if($get_host =~ /$_/){&error("恐れ入りますがご利用中のホストからはアクセスできません");}
		if($get_addr =~ /$_/){&error("恐れ入りますがご利用中のホストからはアクセスできません");}
		if ($_ eq "") { next; }
		$_ =~ s/\*/\.\*/g;
		if ($get_host =~ /$_/i) { &error("恐れ入りますがご利用中のホストからはアクセスできません"); }
		if ($get_addr =~ /$_/i) { &error("恐れ入りますがご利用中のホストからはアクセスできません"); }
	}


	#=====GETでのアクセスを拒否=====#
	if($in{'mode'} ne "" && $in{'mode'} ne "houmon" && $in{'ori_ie_id'} ne "admin" && $in{'mode'} ne "parts_taiou_hyou" && $in{'mode'} ne "itiran" && $in{'mode'} ne "kensaku" && $in{'command'} ne "idousyuuryou" && $in{'command'} ne "easySerch" && $ENV{'SCRIPT_NAME'}!~/bbs.cgi/ && $ENV{'SCRIPT_NAME'}!~/item.cgi/){
			if ($ENV{'REQUEST_METHOD'} ne "POST") {
				&error("GETは受け付けておりません");
			}
	}
	
	#=====パスワードチェック=====#
	if ($in{'admin_pass'} ne $admin_pass and $in{'admin_pass'} ne $admin_pass2){
		if($in{'mode'} ne "" && $in{'mode'} ne "new" && $in{'mode'} ne "parts_taiou_hyou" && $in{'mode'} ne "new_hyouji" && $ENV{'SCRIPT_NAME'}!~/item.cgi/){
			&check_pass;
		}
	}
	
	#=====参加者表示時の優遇=====#
	if($hyogi_yuguu eq 'yes' && $name){
		open(GUEST,"< $guestfile");
		eval{ flock (GUEST, 1); };
		@all_guest=<GUEST>;
		close(GUEST);
		if ($in{'sanka_hyouzi_on'} eq 'on' && $name ne ""){
			$koudou_seigen = $yuguujikan;
		}else{
			foreach(@all_guest){
				($sanka_timer,$sanka_name,$hyouzi_check,$mati_name) = split(/<>/);
				if($sanka_name eq $name && $hyouzi_check eq 'on'){
					$koudou_seigen = $yuguujikan;
					last;
				}
			}
		}
	}

	#=====特別な制限時間=====#
	if ($seigen{$name} ne ""){
		$koudou_seigen = $seigen{$name};
	}
	if($k_id){
		$monokiroku_file="./member/$k_id/mono.cgi";
		open(OUT,"$monokiroku_file") || &error("自分の購入物ファイルが開けません");
		eval{ flock (OUT, 2); };
		@my_kounyuu_list =<OUT>;
		close(OUT);
		foreach (@my_kounyuu_list){
			&syouhin_sprit ($_);
			if ($syo_hinmoku eq '仕事の友'){
				$work_seigen_time = 3;
				last;
			}
		}
	}

	if ($work_seigen{$name} ne ""){$work_seigen_time = $work_seigen{$name};}
	
	#===== アクセスログ残す =====#
	$access_file = "./member/$k_id/access.cgi";
	$access_genkai = "25";
	
	if (! -e $access_file){
		open(ME,">$access_file") || &error("Write Error : $access_file");
		eval{ flock (ME, 2); };
		chmod 0666,"$access_file";
		close(ME);
	}
	
	open(IN,"<$access_file") || &error("$access_fileが開けません");
	eval{ flock (IN, 2); };
	@access_data = <IN>;
	if ($#access_data >= $access_genkai-1){
		$#access_data = $access_genkai-1;
	}
	close(IN);
	
	&get_host;
	$now = time;
	push(@access_data,"$return_host<>$now\n");
	
	open(OUT,">$access_file") || &error("Write Error : $access_file");
	eval{ flock (OUT, 2); };
	print OUT @access_data;
	close(OUT);
}

#---------------多重チェック処理-------------------#
sub tajuucheck {
	foreach (@tazyu_kyoka){if ($name eq $_){return;}}
	&get_host;
	open(IN,"< $logfile") || &error("Open Error : $logfile");
	eval{ flock (IN, 1); };
	@rankingMember = <IN>;
	close(IN);

	foreach (@rankingMember) {
		($list_k_id,$list_name,$list_pass,$list_money,$list_bank,$list_job,$list_kokugo,$list_suugaku,$list_rika,$list_syakai,$list_eigo,$list_ongaku,$list_bijutu,$list_looks,$list_tairyoku,$list_kenkou,$list_speed,$list_power,$list_wanryoku,$list_kyakuryoku,$list_love,$list_unique,$list_etti,$list_first_access,$list_kounyuu,$list_sex,$list_access_byou,$list_access_time,$list_host)= split(/<>/);
		if ($list_name eq $name){next;}
		if($return_host eq $list_host && $in{'admin_pass'} ne "$admin_pass" && $pass ne "$admin_pass"){
			$k_yobi3 = "$list_name：$name";
			&temp_routin;
			&log_kousin($my_log_file,$k_temp);	
			
			&openAitelog ($list_k_id);
			$aite_yobi3 = "$list_name：$name";
			&aite_temp_routin;
			&lock;
			open(OUT,">$aite_log_file") || &error("$aite_log_fileが開けません3");
			eval{ flock (OUT, 2); };
			print OUT $aite_k_temp;
			close(OUT);
			&unlock;
			&error("多重登録は禁止されています。この記録は保存されました。<br>$list_name：$name");
		}
	}	
}

#---------------記帳処理-------------------#
sub kityou_syori {
	local(@my_tuutyou);
	$ginkoumeisai_file="./member/$k_id/ginkoumeisai.cgi";
	open(GM,"< $ginkoumeisai_file") || &error("自分の預金通帳ファイルが開けません");
	eval{ flock (GM, 1); };
	@my_tuutyou = <GM>;
	close(GM);
	&time_get;
	if(!$date){
		$date_sec = time ;
		($sec0,$min0,$hour0,$mday0,$mon0,$year0) = localtime($date_sec);
		$date_kityou = sprintf("%04d/%02d/%02d",$year0+1900,$mon0+1,$mday0);
		$date = $date_kityou;
	}
	$torihikinaiyou = "$date<>$_[0]<>$_[1]<>$_[2]<>$_[3]<>$_[4]<>\n";
	#(日付,"明細",出金額,入金額,残高,普or定)
	unshift (@my_tuutyou,$torihikinaiyou);
	$meisai_kensuu = @my_tuutyou;
	if ($meisai_kensuu > 100){pop (@my_tuutyou);}
	&lock;
	open(GMO,">$ginkoumeisai_file") || &error("自分の預金通帳ファイルに書き込めません");
	eval{ flock (GMO, 2); };
	print GMO @my_tuutyou;
	close(GMO);
	&unlock;
}

#---------------相手の記帳処理-------------------#
sub aite_kityou_syori {
	my (@aite_tuutyou);
	if (@_[6] ne "lock_off"){
		&lock;
	}
	$ginkoumeisai_file="./member/@_[5]/ginkoumeisai.cgi";
	open(GM,"< $ginkoumeisai_file") || &error("相手の預金通帳ファイルが開けません");
	eval{ flock (GM, 1); };
	@aite_tuutyou = <GM>;
	close(GM);
	&time_get;
	$torihikinaiyou = "$date<>@_[0]<>@_[1]<>@_[2]<>@_[3]<>@_[4]<>\n";
	#("明細",出金額,入金額,残高,普or定,振込先ID,"lock_off or 無し")
	unshift (@aite_tuutyou,$torihikinaiyou);
	$meisai_kensuu = @aite_tuutyou;
	if ($meisai_kensuu > 100){pop (@aite_tuutyou);}
	open(GMO,">$ginkoumeisai_file") || &error("相手の預金通帳ファイルに書き込めません");
	eval{ flock (GMO, 2); };
	print GMO @aite_tuutyou;
	close(GMO);
	if (@_[6] ne "lock_off"){
		&unlock;
	}
}

#---------------ニュース記録-------------------#
sub news_kiroku {
	&time_get;
	open(NS,"< $news_file") || &error("$news_fileが開けません。");
	eval{ flock (NS, 1); };
	@town_news = <NS>;
	close(NS);
	$new_news_kizi = "$date2<>@_[0]<>@_[1]<>\n";
	unshift (@town_news,$new_news_kizi);
	$i = 0;
	@new_town_news = ();
	foreach (@town_news){
		push (@new_town_news,$_);
		$i ++;
		if ($i >= $news_kensuu){last;}
	}
	open(NSO,">$news_file") || &error("$news_fileに書き込めません");
	eval{ flock (NSO, 2); };
	print NSO @new_town_news;
	close(NSO);
}

#---------------住んでいる街のチェック-------------------#
sub my_town_check {
		open(MTC,"< $ori_ie_list") || &error("Open Error : $ori_ie_list");
		eval{ flock (MTC, 1); };
		my @ori_ie_para = <MTC>;
		close(MTC);
		$my_town_ari = 0;
		foreach (@ori_ie_para){
			my ($ori_k_id,$ori_ie_name,$ori_ie_setumei,$ori_ie_image,$ori_ie_syubetu,$ori_ie_kentikubi,$ori_ie_town)= split(/<>/);
			if (@_[0] eq "$ori_ie_name"){
				$return_my_town = "$ori_ie_town";
				$my_town_ari = 1;
				last;
			}
		}
		if ($my_town_ari == 0){$return_my_town = "no_town";}
}

#---------------街の経済力アップ-------------------#
sub town_keizaiup {
	my $town_data = "./log_dir/townlog".@_[1].".cgi";
	open(TW,"< $town_data") || &error("Open Error : $town_data");
	eval{ flock (TW, 1); };
	my $keizai_town_hairetu = <TW>;
	close(TW);
		my @town_sprit_matrix =  split(/<>/,$keizai_town_hairetu);
		if ($town_sprit_matrix[260]  == ""){$town_sprit_matrix[260] = time;}
		$town_sprit_matrix[2] += @_[0];
		my $town_temp=join("<>",@town_sprit_matrix);
		
#==========タウン情報更新=============
	open(TWO,">$town_data") || &error("$town_dataに書き込めません");
	eval{ flock (TWO, 2); };
	print TWO $town_temp;
	close(TWO);

#==========メインタウン情報の更新=============
	open(MT,"< $maintown_logfile") || &error("Open Error : $maintown_logfile");
	eval{ flock (MT, 1); };
	my $maintown_para = <MT>;
	close(MT);
	my @main_town_sprit_matrix =  split(/<>/,$maintown_para);
	if ($main_town_sprit_matrix[10]  == ""){$main_town_sprit_matrix[10] = time;}
		$main_town_sprit_matrix[1] += @_[0];
		$main_town_temp=join("<>",@main_town_sprit_matrix);
			open(OUT,">$maintown_logfile") || &error("Write Error : $maintown_logfile");
			eval{ flock (OUT, 2); };
			print OUT $main_town_temp;
			close(OUT);	
}

#---------------街の繁栄度アップ-------------------#
sub town_haneiup {
	my $town_data = "./log_dir/townlog".@_[0].".cgi";
	open(TW,"< $town_data") || &error("Open Error : $town_data");
	eval{ flock (TW, 1); };
	my $keizai_town_hairetu = <TW>;
	close(TW);
	my @town_sprit_matrix =  split(/<>/,$keizai_town_hairetu);
	if ($town_sprit_matrix[260]  == ""){$town_sprit_matrix[260] = time;}
	$town_sprit_matrix[3] ++ ;
	my $town_temp=join("<>",@town_sprit_matrix);
		
#==========タウン情報更新=============
	open(TWO,">$town_data") || &error("$town_dataに書き込めません");
	eval{ flock (TWO, 2); };
	print TWO $town_temp;
	close(TWO);

#==========メインタウン情報の更新=============
	open(MT,"< $maintown_logfile") || &error("Open Error : $maintown_logfile");
	eval{ flock (MT, 1); };
	my $maintown_para = <MT>;
	close(MT);
	my @main_town_sprit_matrix =  split(/<>/,$maintown_para);
	if ($main_town_sprit_matrix[10]  == ""){$main_town_sprit_matrix[10] = time;}
		$main_town_sprit_matrix[2] ++ ;
		$main_town_temp=join("<>",@main_town_sprit_matrix);
			open(OUT,">$maintown_logfile") || &error("Write Error : $maintown_logfile");
			eval{ flock (OUT, 2); };
			print OUT $main_town_temp;
			close(OUT);
}

#---------------データ保存-------------------#
sub data_save {
	my($data_path, @WRITE_DATA) = @_;
	my($err) = '';
	$data_path =~ /(.+)\..+$/;
	my($filename) = $1;
	if ($filename !~ /.+/) { $err = 'bad Filename(Not Extension?)'; }
	if (!$err) {
		my($tmpfile) = "$filename.tmp";
		my($tmpflag) = 0;
		foreach (1 .. 10) {
			unless (-f $tmpfile) { $tmpflag = 1; last; }
			$tmpflag = 0;
			for (0..50){$i=0;}
		}
		if ($tmpflag) {
			$tmp_dummy = "$$\.tmp";
			if (!open(TMP,">$tmp_dummy")) { $err = 'bad New TemporaryFile'; }
			eval{ flock (TMP, 2); };
			if (!$err) {
				close(TMP);
				chmod 0666,$tmp_dummy;
				if (!open(TMP,">$tmp_dummy")) { $err = 'bad New TemporaryFile'; }
				eval{ flock (TMP, 2); };
				if (!$err) {
					binmode TMP;
					print TMP @WRITE_DATA;
					close(TMP);
					foreach (1 .. 10) {
						unless (-f $tmpfile) {
							if (!open(TMP,">$tmpfile")) {
								eval{ flock (TMP, 2); };
								$err = 'bad LockFile System';
								last;
							}
							if (!$err) {
								close(TMP);
								rename($tmp_dummy, $data_path);
								unlink $tmpfile;
								last;
							}
						}
						for (0..50){$i=0;}
					}
				}
			}
		}
	}
	return $err;
}

#---------------データ読み込み-------------------#
sub data_read {
	my($data_path) = @_;
	my(@READ_DATA);
	if (open(DB,"< $data_path")) {
		eval{ flock (DB, 1); };
		@READ_DATA = <DB>;
		close(DB);
	}
	return @READ_DATA;
}

#---------------自立後の子供からの仕送り-------------------#
sub kodomo_siokuri {
#==========職業ごとの給料をハッシュに代入=============
	open(SP,"< ./dat_dir/job.cgi") || &error("Open Error : ./dat_dir/job.cgi");
	eval{ flock (SP, 1); };
	$top_koumoku = <SP>;
	@job_hairetu = <SP>;
	close(SP);
	foreach  (@job_hairetu) {
		&job_sprit($_);
		$job_kihonkyuu {$job_name} = $job_kyuuyo;
	}
	open(KOD,"< $kodomo_file") || &error("Open Error : $kodomo_file");
	eval{ flock (KOD, 1); };
	@all_kodomo=<KOD>;
	close(KOD);
	$now_time= time;
	$kodomoiruka_flag=0;
	foreach  (@all_kodomo) {
		($kod_num,$kod_name,$kod_oya1,$kod_oya2,$kod_job,$kod_kokugo,$kod_suugaku,$kod_rika,$kod_syakai,$kod_eigo,$kod_ongaku,$kod_bijutu,$kod_looks,$kod_tairyoku,$kod_kenkou,$kod_speed,$kod_power,$kod_wanryoku,$kod_kyakuryoku,$kod_love,$kod_unique,$kod_etti,$kod_yobi1,$kod_yobi2,$kod_yobi3,$kod_yobi4,$kod_yobi5,$kod_yobi6,$kod_yobi7,$kod_yobi8,$kod_yobi9,$kod_yobi10)=split(/<>/);
		if ($kod_yobi8 != 1){next;}
		if ($kod_oya1 eq $name || $kod_oya2 eq $name){
				$kono_nenrei = int (($now_time - $kod_yobi1)/(60*60*24));
				$siokuri_kingaku = ($job_kihonkyuu {$kod_job} * $kono_nenrei) + ($kod_yobi4 * 10);
				$siokuri_kingaku = int ($siokuri_kingaku / 4);
				$bank += $siokuri_kingaku;
				&kityou_syori("仕送り←$kod_name","",$siokuri_kingaku,$bank,"普");
		}
	}
}

#---------------運営会社からの所得-------------------#
sub unei_siokuri {
	$unei_file="./member/$k_id/1_log.cgi";
	if (! -e $unei_file){return;}
	open(KOD,"< $unei_file") || &error("Open Error : $unei_file");
	eval{ flock (KOD, 1); };
	$all_une = <KOD>;
	close(KOD);

	($unei_num,$unei_name,$unei_oya1,$unei_oya2,$unei_job,$unei_kokugo,$unei_suugaku,$unei_rika,$unei_syakai,$unei_eigo,$unei_ongaku,$unei_bijutu,$unei_looks,$unei_tairyoku,$unei_kenkou,$unei_speed,$unei_power,$unei_wanryoku,$unei_kyakuryoku,$unei_love,$unei_unique,$unei_etti,$unei_yobi1,$unei_yobi2,$unei_yobi3,$unei_yobi4,$unei_yobi5,$unei_yobi6,$unei_yobi7,$unei_yobi8,$unei_yobi9,$ori_ie_rank)=split(/<>/, $all_une);
	$siokuri_kingaku1 = ($job_kihonkyuu{"$unei_job"} * 10) + ($unei_yobi4 * 10);
	$siokuri_kingaku1 = int ($siokuri_kingaku1 / 4);
	$bank += $siokuri_kingaku1;
	&kityou_syori("収入←運営($unei_job)","",$siokuri_kingaku1,$bank,"普");

}

#---------------運営会社からの所得２-------------------#
sub unei_siokuri2 {
	$unei_file="./member/$k_id/1_log.cgi";
	if (! -e $unei_file){return;}
	open(KOD,"< $unei_file") || &error("Open Error : $unei_file");
	eval{ flock (KOD, 1); };
	@all_une = <KOD>;
	close(KOD);

	foreach (@all_une){
		($unei_num,$unei_name,$unei_oya1,$unei_oya2,$unei_job,$unei_kokugo,$unei_suugaku,$unei_rika,$unei_syakai,$unei_eigo,$unei_ongaku,$unei_bijutu,$unei_looks,$unei_tairyoku,$unei_kenkou,$unei_speed,$unei_power,$unei_wanryoku,$unei_kyakuryoku,$unei_love,$unei_unique,$unei_etti,$unei_yobi1,$unei_yobi2,$unei_yobi3,$unei_yobi4,$unei_yobi5,$unei_yobi6,$unei_yobi7,$unei_yobi8,$unei_yobi9,$ori_ie_rank)=split(/<>/);
		$siokuri_kingaku1 = ($job_kihonkyuu{"$unei_job"} * 10) + ($unei_yobi4 * 10);
		$siokuri_kingaku1 = int ($siokuri_kingaku1 / 4);
		$siokuri_kingaku2 += $siokuri_kingaku1;
	}

	$bank += $siokuri_kingaku2;
	&kityou_syori("収入←運営","",$siokuri_kingaku2,$bank,"普");

}

#---------------会社収益-------------------#
sub unei_siokuri3 {
	$unei_file="./member/$k_id/2_log.cgi";
	if (! -e $unei_file){return;}
	open(KOD,"< $unei_file") || &error("Open Error : $unei_file");
	eval{ flock (KOD, 1); };
	@all_une = <KOD>;
	close(KOD);

	foreach (@all_une){
		($unei_num,$unei_name,$unei_oya1,$unei_oya2,$unei_job,$unei_kokugo,$unei_suugaku,$unei_rika,$unei_syakai,$unei_eigo,$unei_ongaku,$unei_bijutu,$unei_looks,$unei_tairyoku,$unei_kenkou,$unei_speed,$unei_power,$unei_wanryoku,$unei_kyakuryoku,$unei_love,$unei_unique,$unei_etti,$unei_yobi1,$unei_yobi2,$unei_yobi3,$unei_yobi4,$unei_yobi5,$unei_yobi6,$unei_yobi7,$unei_yobi8,$unei_yobi9,$ori_ie_rank)=split(/<>/);
		$siokuri_kingaku1 = ($job_kihonkyuu{"$unei_job"} * 10) + ($unei_yobi4 * 10);
		$siokuri_kingaku1 = int ($siokuri_kingaku1 / 4);
		$siokuri_kingaku2 += $siokuri_kingaku1;
	}

	$bank += $siokuri_kingaku2;
	&kityou_syori("収入←自分の会社","",$siokuri_kingaku2,$bank,"普");

	open (KAISYA,"< ./member/$k_id/kaishiya_kanri.cgi") || &error("Open Error : ./member/$k_id/kaishiya_kanri.cgi");
	eval{ flock (KAISYA, 1); };
	$ouna = <KAISYA>;
	@yakuin_list = <KAISYA>;
	close(KAISYA);

	($kai_id_o,$kai_name_o,$kai_time_o) = split(/<>/,$ouna);

	$f_chngi = 0;
	@yakuin0_list = ();
	foreach (@yakuin_list){
		($aite_id,$kai_name,$kai_time) = split(/<>/);
		$aite_log_file = "./member/$aite_id/log.cgi";
		if (! -e $aite_log_file){$f_chngi = 1;next;}
		open(AIT,"< $aite_log_file") || &error("$aite_log_fileが開けません。");
		eval{ flock (AIT, 1); };
		$aite_prof = <AIT>;
		if($aite_prof == ""){close(AIT);$f_chngi = 1;next;}
		&aite_sprit($aite_prof);
		close(AIT);
		$aite_bank += $siokuri_kingaku2;
		&aite_temp_routin;
		open(OUT,">$aite_log_file") || &error("$aite_log_fileが開けません5");
		eval{ flock (OUT, 2); };
		print OUT $aite_k_temp;
		close(OUT);
		&aite_kityou_syori("収入←$kai_name_oの会社","",$siokuri_kingaku2,$aite_bank,"普",$aite_id);
		push @yakuin0_list,"$aite_id<>$kai_name<>$kai_time<>\n";
	}
	if($f_chngi){
		open (KAISYA,"> ./member/$kai_id_o/kaishiya_kanri.cgi") || &error("Open Error : ./member/$kai_id_o/kaishiya_kanri.cgi");
		eval{ flock (KAISYA, 2); };
		print KAISYA $ouna;
		print KAISYA @yakuin0_list;
		close(KAISYA);
	}
}

#-----アイテムゲット-----#
sub item_get{
	($syo_syubetu0,$syo_hinmoku0,$syo_kokugo0,$syo_suugaku0,$syo_rika0,$syo_syakai0,$syo_eigo0,$syo_ongaku0,$syo_bijutu0,$syo_kouka0,$syo_looks0,$syo_tairyoku0,$syo_kenkou0,$syo_speed0,$syo_power0,$syo_wanryoku0,$syo_kyakuryoku0,$syo_nedan0,$syo_love0,$syo_unique0,$syo_etti0,$syo_taikyuu0,$syo_taikyuu_tani0,$syo_kankaku0,$syo_zaiko0,$syo_cal0,$syo_siyou_date0,$syo_sintai_syouhi0,$syo_zunou_syouhi0,$syo_comment0,$syo_kounyuubi0,$tanka0,$tokubai)= split(/<>/,@_[0]);
	
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,"< $monokiroku_file") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 2); };
	@my_kounyuu_list =<OUT>;
	close(OUT);
	
	if (@my_kounyuu_list >= $syoyuu_gendosuu){$kensa_flag=2;return;}
	
	$kensa_flag=0;
	@new_myitem_hairetu = ();
	foreach $one_kounyuu_item (@my_kounyuu_list){
		&syouhin_sprit ($one_kounyuu_item);
		if ($syo_syubetu eq $syo_syubetu0 && $syo_hinmoku eq $syo_hinmoku0){
			$syo_taikyuu += $syo_taikyuu0;
			$kensa_flag = 1;
		}
		&syouhin_temp;
		push @new_myitem_hairetu,$syo_temp;
	}
	if ($kensa_flag != 1){
		$syo_kounyuubi0 = time;
		$syo_temp0="$syo_syubetu0<>$syo_hinmoku0<>$syo_kokugo0<>$syo_suugaku0<>$syo_rika0<>$syo_syakai0<>$syo_eigo0<>$syo_ongaku0<>$syo_bijutu0<>$syo_kouka0<>$syo_looks0<>$syo_tairyoku0<>$syo_kenkou0<>$syo_speed0<>$syo_power0<>$syo_wanryoku0<>$syo_kyakuryoku0<>$syo_nedan0<>$syo_love0<>$syo_unique0<>$syo_etti0<>$syo_taikyuu0<>$syo_taikyuu_tani0<>$syo_kankaku0<>$syo_zaiko0<>$syo_cal0<>$syo_siyou_date0<>$syo_sintai_syouhi0<>$syo_zunou_syouhi0<>$syo_comment0<>$syo_kounyuubi0<>$tanka0<>$tokubai0<>\n";
		push @new_myitem_hairetu,$syo_temp0;
	}
	open(OUT,">$monokiroku_file") || &error("Write Error : $monokiroku_file");
	eval{ flock (OUT, 2); };
	print OUT @new_myitem_hairetu;
	close(OUT);
}

1;