#!/usr/bin/perl

$this_script = 'admin2.cgi';
require './town_ini.cgi';
require './town_lib.pl';
require './unit.pl';
&decode;

##############################\
#各街のパスワード設定
$town_pass0="";
$town_pass1="";
$town_pass2="";
$town_pass3="";
##############################

#==========メンテチェック==========#
	if($mente_flag == 1 && $in{'admin_pass'} eq "" && $in{'mode'} ne ""){&error("$mente_message")}
$seigenyou_now_time = time;
	
#==========制限時間チェック==========#
		$ato_nanbyou=$koudou_seigen-($seigenyou_now_time - $access_byou);
		if($seigenyou_now_time - $access_byou < $koudou_seigen){&error("まだ行動できません。あと$ato_nanbyou秒お待ちください。")}
		
#===========条件分岐==========#
	if($in{'mode'} eq "admin"){&admin;}
	elsif($in{'mode'} eq "admin_bbs"){&admin_bbs;}
	elsif($in{'mode'} eq "bbs1_settei_do"){&bbs1_settei_do;}
	elsif($in{'mode'} eq "ad_orosi_kousin"){&ad_orosi_kousin;}
	elsif($in{'mode'} eq "parts_taiou_hyou"){&parts_taiou_hyou;}
	elsif($in{'mode'} eq "itiran"){&itiran;}
	elsif($in{'mode'} eq "make_town"){&make_town;}
	elsif($in{'mode'} eq "depaato_kousin"){&depaato_kousin;}
	elsif($in{'mode'} eq "mail_soshin"){&mail_soshin;}
	else{&error("「戻る」ボタンで街に戻ってください");}
	
exit;
	
####################################################
#/////////////////以下サブルーチン/////////////////#
####################################################

#----------管理画面----------#
sub admin {

#==========パスワード入力画面==========#
    if ($in{'admin_pass'} eq ""){
	&header;
	print <<"EOM";
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="admin">
	<br><div align=center>
	パスワードを入力してください。<br><br>
	<input type=text name="admin_pass" size=10><input type=submit value="OK"></div>
	</form>
EOM
exit;
    }
    
	if ($in{'admin_pass'} ne $admin_pass2){&error("パスワードが違います");}
	
		$refe = $ENV{'HTTP_REFERER'};
	if ($refe !~ /$setti1/ && $refe !~ /$setti2/ && $refe !~ /$setti3/){
	&error("トップページより正しくお入りください。<br>$refe");}
	
#==========画面出力==========#
	&header;
	print <<"EOM";
	<div align=center class=midasi>管理者メニュー</div><br>
	<table width="500" border="0" cellspacing="0" cellpadding="10" align=center>
  <tr><td>
  <div class=tyuu>●街のレイアウト作成</div>
EOM
 	$i=0;
 	foreach (@town_hairetu) {
			 print <<"EOM";
			<form method="POST" action="$this_script">
			<input type=hidden name=mode value="make_town">
			<input type=hidden name=command value="m_form">
			<input type=hidden name=admin_pass value="$in{'admin_pass'}">
			<input type=hidden name=town_no value="$i">
			<input type=hidden name=town_n value="$_">
			<input type=text name=town_pass size="8">
			<input type=submit value="『$_』のレイアウト作成">
			</form>
EOM
 			$i ++;
  	}
	 print "<hr size=1>";
	 print "<div class=tyuu>●管理者作成BBSの設定</div>";
 	$i=0;
 	foreach (@admin_bbs_syurui) {
			 print <<"EOM";
			<form method="POST" action="$this_script">
			<input type=hidden name=mode value="admin_bbs">
			<input type=hidden name=bbs_num value="$i">
			<input type=hidden name=admin_pass value="$in{'admin_pass'}">
			<input type=submit value="$_の設定">
			</form>
EOM
 			$i ++;
  	}
	 
  print <<"EOM";
	<hr size=1>
		  	<div class=tyuu>●メンバー管理</div>
  			<form method="POST" action="$this_script">
			<input type=hidden name=mode value="itiran">
			<input type=hidden name=sort_id value="0">
 			<input type=hidden name=admin_pass value="$in{'admin_pass'}">
			<input type=submit value="登録者一覧（ランキング）">
			</form>
  	<hr size=1>
		  	<div class=tyuu>●一斉メール</div>
  			<form method="POST" action="$this_script">
			<input type=hidden name=mode value="mail_soshin">
			<input type=hidden name=name value="$in{'name'}">
			<input type=hidden name=sort_id value="0">
			<textarea name=isseimail rows=5 cols=80></textarea>
			<input type=hidden name=admin_pass value="$in{'admin_pass'}">
			<input type=submit value="一斉メール送信">
			</form>
	<hr size=1>
	  ※ver.1.2より個人データのバックアップデータはmemberディレクトリ内の「ID番号＋backup」ディレクトリに保存されています。またこのディレクトリは削除期限が過ぎてその人のデータが削除された後も残る仕様になっていますので、たまにbackupのみとなったディレクトリを削除するようにしてください。<br>
	  ※個人データ以外の各種ログ（log_dirフォルダー内のファイル）は１日１回バックアップ処理が行われています。全てのログファイルは、「log_dir」フォルダー内の「backup_dir」フォルダーに頭に「backup_」がついたファイル名で保存されています。現状、復活に関するコマンドは用意しておりませんので、万が一ログが消失するようなことがあった場合、該当するファイルをこのバックアップファイルからコピーするなどしてお使いください。

  	<hr size=1>
		  	<div class=tyuu>●卸商品の更新</div>
			  ※このボタンを押すことで管理者が任意の時間に卸商品を更新することができます。
  			<form method="POST" action="$this_script">
			<input type=hidden name=mode value="ad_orosi_kousin">
			<input type=hidden name=admin_pass value="$in{'admin_pass'}">
			<input type=submit value="更新する">
			</form>
  	<hr size=1>
		  	<div class=tyuu>●デパート・食堂の更新</div>
			  ※このボタンを押すことで管理者が任意の時間に卸商品を更新することができます。
  			<form method="POST" action="$this_script">
			<input type=hidden name=mode value="depaato_kousin">
			<input type=hidden name=admin_pass value="$in{'admin_pass'}">
			<input type=submit value="更新する">
			</form>
  	<hr size=1>
	</td></tr></table>
	<div align=center><a href=$script>[戻る]</a></div>
	</body></html>
EOM
exit;
}

#----------（仮？）街レイアウトのログファイル作成----------#
sub town_temp{
$town_temp = "$town_name<>$zinkou<>$keizai<>$hanei<>$t_x0<>$t_x1<>$t_x2<>$t_x3<>$t_x4<>$t_x5<>$t_x6<>$t_x7<>$t_x8<>$t_x9<>$t_x10<>$t_x11<>$t_x12<>$t_x13<>$t_x14<>$t_x15<>$t_x16<>$t_a0<>$t_a1<>$t_a2<>$t_a3<>$t_a4<>$t_a5<>$t_a6<>$t_a7<>$t_a8<>$t_a9<>$t_a10<>$t_a11<>$t_a12<>$t_a13<>$t_a14<>$t_a15<>$t_a16<>$t_b0<>$t_b1<>$t_b2<>$t_b3<>$t_b4<>$t_b5<>$t_b6<>$t_b7<>$t_b8<>$t_b9<>$t_b10<>$t_b11<>$t_b12<>$t_b13<>$t_b14<>$t_b15<>$t_b16<>$t_c0<>$t_c1<>$t_c2<>$t_c3<>$t_c4<>$t_c5<>$t_c6<>$t_c7<>$t_c8<>$t_c9<>$t_c10<>$t_c11<>$t_c12<>$t_c13<>$t_c14<>$t_c15<>$t_c16<>$t_d0<>$t_d1<>$t_d2<>$t_d3<>$t_d4<>$t_d5<>$t_d6<>$t_d7<>$t_d8<>$t_d9<>$t_d10<>$t_d11<>$t_d12<>$t_d13<>$t_d14<>$t_d15<>$t_d16<>$t_e0<>$t_e1<>$t_e2<>$t_e3<>$t_e4<>$t_e5<>$t_e6<>$t_e7<>$t_e8<>$t_e9<>$t_e10<>$t_e11<>$t_e12<>$t_e13<>$t_e14<>$t_e15<>$t_e16<>$t_f0<>$t_f1<>$t_f2<>$t_f3<>$t_f4<>$t_f5<>$t_f6<>$t_f7<>$t_f8<>$t_f9<>$t_f10<>$t_f11<>$t_f12<>$t_f13<>$t_f14<>$t_f15<>$t_f16<>$t_g0<>$t_g1<>$t_g2<>$t_g3<>$t_g4<>$t_g5<>$t_g6<>$t_g7<>$t_g8<>$t_g9<>$t_g10<>$t_g11<>$t_g12<>$t_g13<>$t_g14<>$t_g15<>$t_g16<>$t_h0<>$t_h1<>$t_h2<>$t_h3<>$t_h4<>$t_h5<>$t_h6<>$t_h7<>$t_h8<>$t_h9<>$t_h10<>$t_h11<>$t_h12<>$t_h13<>$t_h14<>$t_h15<>$t_h16<>$t_i0<>$t_i1<>$t_i2<>$t_i3<>$t_i4<>$t_i5<>$t_i6<>$t_i7<>$t_i8<>$t_i9<>$t_i10<>$t_i11<>$t_i12<>$t_i13<>$t_i14<>$t_i15<>$t_i16<>$t_j0<>$t_j1<>$t_j2<>$t_j3<>$t_j4<>$t_j5<>$t_j6<>$t_j7<>$t_j8<>$t_j9<>$t_j10<>$t_j11<>$t_j12<>$t_j13<>$t_j14<>$t_j15<>$t_j16<>$t_k0<>$t_k1<>$t_k2<>$t_k3<>$t_k4<>$t_k5<>$t_k6<>$t_k7<>$t_k8<>$t_k9<>$t_k10<>$t_k11<>$t_k12<>$t_k13<>$t_k14<>$t_k15<>$t_k16<>$t_l0<>$t_l1<>$t_l2<>$t_l3<>$t_l4<>$t_l5<>$t_l6<>$t_l7<>$t_l8<>$t_l9<>$t_l10<>$t_l11<>$t_l12<>$t_l13<>$t_l14<>$t_l15<>$t_l16<>$t_m0<>$t_m1<>$t_m2<>$t_m3<>$t_m4<>$t_m5<>$t_m6<>$t_m7<>$t_m8<>$t_m9<>$t_m10<>$t_m11<>$t_m12<>$t_m13<>$t_m14<>$t_m15<>$t_m16<>$t_n0<>$t_n1<>$t_n2<>$t_n3<>$t_n4<>$t_n5<>$t_n6<>$t_n7<>$t_n8<>$t_n9<>$t_n10<>$t_n11<>$t_n12<>$t_n13<>$t_n14<>$t_n15<>$t_n16<>$tika<>$t_yobi2<>$t_yobi3<>$t_yobi4<>$t_yobi5<>$t_yobi6<>$t_yobi7<>\n";
}

#----------街レイアウトのログファイル作成----------#
sub make_town {
	if ($in{'admin_pass'} ne $admin_pass2){&error("パスワードが違います");}
		&header(2);
	if($in{'command'} eq "m_form"){
	if($in{'town_no'}==0 && $in{'town_pass'} ne $town_pass0){&error("パスワードが違います");}
	if($in{'town_no'}==1 && $in{'town_pass'} ne $town_pass1){&error("パスワードが違います");}
	if($in{'town_no'}==2 && $in{'town_pass'} ne $town_pass2){&error("パスワードが違います");}
	if($in{'town_no'}==3 && $in{'town_pass'} ne $town_pass3){&error("パスワードが違います");}
		&town_form;
		exit;
	}
	if($in{'command'} eq "regi"){
$town_temp = "$in{'town_n'}<>$in{'zinkou'}<>$in{'keizai'}<>$in{'hanei'}<>$in{'t_x0'}<>$in{'t_x1'}<>$in{'t_x2'}<>$in{'t_x3'}<>$in{'t_x4'}<>$in{'t_x5'}<>$in{'t_x6'}<>$in{'t_x7'}<>$in{'t_x8'}<>$in{'t_x9'}<>$in{'t_x10'}<>$in{'t_x11'}<>$in{'t_x12'}<>$in{'t_x13'}<>$in{'t_x14'}<>$in{'t_x15'}<>$in{'t_x16'}<>$in{'t_a0'}<>$in{'t_a1'}<>$in{'t_a2'}<>$in{'t_a3'}<>$in{'t_a4'}<>$in{'t_a5'}<>$in{'t_a6'}<>$in{'t_a7'}<>$in{'t_a8'}<>$in{'t_a9'}<>$in{'t_a10'}<>$in{'t_a11'}<>$in{'t_a12'}<>$in{'t_a13'}<>$in{'t_a14'}<>$in{'t_a15'}<>$in{'t_a16'}<>$in{'t_b0'}<>$in{'t_b1'}<>$in{'t_b2'}<>$in{'t_b3'}<>$in{'t_b4'}<>$in{'t_b5'}<>$in{'t_b6'}<>$in{'t_b7'}<>$in{'t_b8'}<>$in{'t_b9'}<>$in{'t_b10'}<>$in{'t_b11'}<>$in{'t_b12'}<>$in{'t_b13'}<>$in{'t_b14'}<>$in{'t_b15'}<>$in{'t_b16'}<>$in{'t_c0'}<>$in{'t_c1'}<>$in{'t_c2'}<>$in{'t_c3'}<>$in{'t_c4'}<>$in{'t_c5'}<>$in{'t_c6'}<>$in{'t_c7'}<>$in{'t_c8'}<>$in{'t_c9'}<>$in{'t_c10'}<>$in{'t_c11'}<>$in{'t_c12'}<>$in{'t_c13'}<>$in{'t_c14'}<>$in{'t_c15'}<>$in{'t_c16'}<>$in{'t_d0'}<>$in{'t_d1'}<>$in{'t_d2'}<>$in{'t_d3'}<>$in{'t_d4'}<>$in{'t_d5'}<>$in{'t_d6'}<>$in{'t_d7'}<>$in{'t_d8'}<>$in{'t_d9'}<>$in{'t_d10'}<>$in{'t_d11'}<>$in{'t_d12'}<>$in{'t_d13'}<>$in{'t_d14'}<>$in{'t_d15'}<>$in{'t_d16'}<>$in{'t_e0'}<>$in{'t_e1'}<>$in{'t_e2'}<>$in{'t_e3'}<>$in{'t_e4'}<>$in{'t_e5'}<>$in{'t_e6'}<>$in{'t_e7'}<>$in{'t_e8'}<>$in{'t_e9'}<>$in{'t_e10'}<>$in{'t_e11'}<>$in{'t_e12'}<>$in{'t_e13'}<>$in{'t_e14'}<>$in{'t_e15'}<>$in{'t_e16'}<>$in{'t_f0'}<>$in{'t_f1'}<>$in{'t_f2'}<>$in{'t_f3'}<>$in{'t_f4'}<>$in{'t_f5'}<>$in{'t_f6'}<>$in{'t_f7'}<>$in{'t_f8'}<>$in{'t_f9'}<>$in{'t_f10'}<>$in{'t_f11'}<>$in{'t_f12'}<>$in{'t_f13'}<>$in{'t_f14'}<>$in{'t_f15'}<>$in{'t_f16'}<>$in{'t_g0'}<>$in{'t_g1'}<>$in{'t_g2'}<>$in{'t_g3'}<>$in{'t_g4'}<>$in{'t_g5'}<>$in{'t_g6'}<>$in{'t_g7'}<>$in{'t_g8'}<>$in{'t_g9'}<>$in{'t_g10'}<>$in{'t_g11'}<>$in{'t_g12'}<>$in{'t_g13'}<>$in{'t_g14'}<>$in{'t_g15'}<>$in{'t_g16'}<>$in{'t_h0'}<>$in{'t_h1'}<>$in{'t_h2'}<>$in{'t_h3'}<>$in{'t_h4'}<>$in{'t_h5'}<>$in{'t_h6'}<>$in{'t_h7'}<>$in{'t_h8'}<>$in{'t_h9'}<>$in{'t_h10'}<>$in{'t_h11'}<>$in{'t_h12'}<>$in{'t_h13'}<>$in{'t_h14'}<>$in{'t_h15'}<>$in{'t_h16'}<>$in{'t_i0'}<>$in{'t_i1'}<>$in{'t_i2'}<>$in{'t_i3'}<>$in{'t_i4'}<>$in{'t_i5'}<>$in{'t_i6'}<>$in{'t_i7'}<>$in{'t_i8'}<>$in{'t_i9'}<>$in{'t_i10'}<>$in{'t_i11'}<>$in{'t_i12'}<>$in{'t_i13'}<>$in{'t_i14'}<>$in{'t_i15'}<>$in{'t_i16'}<>$in{'t_j0'}<>$in{'t_j1'}<>$in{'t_j2'}<>$in{'t_j3'}<>$in{'t_j4'}<>$in{'t_j5'}<>$in{'t_j6'}<>$in{'t_j7'}<>$in{'t_j8'}<>$in{'t_j9'}<>$in{'t_j10'}<>$in{'t_j11'}<>$in{'t_j12'}<>$in{'t_j13'}<>$in{'t_j14'}<>$in{'t_j15'}<>$in{'t_j16'}<>$in{'t_k0'}<>$in{'t_k1'}<>$in{'t_k2'}<>$in{'t_k3'}<>$in{'t_k4'}<>$in{'t_k5'}<>$in{'t_k6'}<>$in{'t_k7'}<>$in{'t_k8'}<>$in{'t_k9'}<>$in{'t_k10'}<>$in{'t_k11'}<>$in{'t_k12'}<>$in{'t_k13'}<>$in{'t_k14'}<>$in{'t_k15'}<>$in{'t_k16'}<>$in{'t_l0'}<>$in{'t_l1'}<>$in{'t_l2'}<>$in{'t_l3'}<>$in{'t_l4'}<>$in{'t_l5'}<>$in{'t_l6'}<>$in{'t_l7'}<>$in{'t_l8'}<>$in{'t_l9'}<>$in{'t_l10'}<>$in{'t_l11'}<>$in{'t_l12'}<>$in{'t_l13'}<>$in{'t_l14'}<>$in{'t_l15'}<>$in{'t_l16'}<>$in{'t_m0'}<>$in{'t_m1'}<>$in{'t_m2'}<>$in{'t_m3'}<>$in{'t_m4'}<>$in{'t_m5'}<>$in{'t_m6'}<>$in{'t_m7'}<>$in{'t_m8'}<>$in{'t_m9'}<>$in{'t_m10'}<>$in{'t_m11'}<>$in{'t_m12'}<>$in{'t_m13'}<>$in{'t_m14'}<>$in{'t_m15'}<>$in{'t_m16'}<>$in{'t_n0'}<>$in{'t_n1'}<>$in{'t_n2'}<>$in{'t_n3'}<>$in{'t_n4'}<>$in{'t_n5'}<>$in{'t_n6'}<>$in{'t_n7'}<>$in{'t_n8'}<>$in{'t_n9'}<>$in{'t_n10'}<>$in{'t_n11'}<>$in{'t_n12'}<>$in{'t_n13'}<>$in{'t_n14'}<>$in{'t_n15'}<>$in{'t_n16'}<>$in{'tika'}<>$in{'t_yobi2'}<>$in{'t_yobi3'}<>$in{'t_yobi4'}<>$in{'t_yobi5'}<>$in{'t_yobi6'}<>$in{'t_yobi7'}<>\n";

						&lock;
						$town_data = "./log_dir/townlog".$in{'town_no'}.".cgi";
						open(KOUT,">$town_data") || &error("Write Error : $town_data");
						eval{ flock (KOUT, 2); };
						print KOUT $town_temp;
						close(KOUT);
						&unlock;
	print <<"EOM";
	<div align=center>$in{'town_n'}を作成しました。<br><br>
	<a href=$script?town_no=$in{'town_no'} target=_blank>[街の確認]</a><br><br>
	<a href=\"javascript:history.back()\"> [前の画面に戻る] </a><br><br>
EOM
	&hooter_a2("admin","戻る","$this_script");
	exit;
	}
}


#----------ＭＡＰ作成画面----------#
sub town_form {
	&get_unit;
	&simaitosi;
	&admin_parts;
	
	if ($in{'admin_pass'} ne $admin_pass2){&error("パスワードが違います");}
	$town_data = "./log_dir/townlog".$in{'town_no'}.".cgi";
	if(! -e $town_data){
		open(INI,">$town_data") || &error("Write Error : $town_data");
		eval{ flock (INI, 2); };
		close(INI);
	}
	open(IN,"$town_data") || &error("Open Error : $town_data");
	eval{ flock (IN, 2); };
	$maketown_data=<IN>;
	close(IN);
			&town_sprit($maketown_data);
	print <<"EOM";
	<table border="0" cellspacing="0" cellpadding="10">
	<tr><td valign=top width=50%>
	<div class="tyuu">$in{'town_n'}のレイアウト作成画面</div>
	このフォームはその入力欄の位置がそのまま街のレイアウトに対応しています。<br>
	右にある表\を参考にして「記号」を入力欄に記述し、OKボタンを押すことで、その場所に記号に対応したパーツが建設されることになります。<br>
	<font color=#ff6600>※設置後、数字のみが入力されていた場合、それは参加者の建築した家です（数字はその方のID）。この数字を変更してしまうと家がなくなってしまったり、街全体に不具合が出てきますので注意してください。</font><br>
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="make_town">
	<input type=hidden name=command value="regi">
	<input type=hidden name=admin_pass value="$in{'admin_pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=hidden name=town_n value="$in{'town_n'}">
	<input type=hidden name=zinkou value="$zinkou">
	<input type=hidden name=keizai value="$keizai">
	<input type=hidden name=hanei value="$hanei">
	<input type=hidden name=t_yobi1 value="$t_yobi1">
	<input type=hidden name=t_yobi2 value="$t_yobi2">
	<input type=hidden name=t_yobi3 value="$t_yobi3">
	<input type=hidden name=t_yobi4 value="$t_yobi4">
	<input type=hidden name=t_yobi5 value="$t_yobi5">
	<input type=hidden name=t_yobi6 value="$t_yobi6">
	<input type=hidden name=t_yobi7 value="$t_yobi7">
		<table border="0" cellspacing="0" cellpadding="0" width=400><!--フォーム用の街スタート-->
        <tr valign="bottom"> <!--横軸の数字出力部分-->
         <td height="10" width="20"  align=center class=sumi></td>
EOM

#==========ヨコの番号部分出力==========#
		 foreach $yokoziku_koumoku (1..16) {
          	print "<td height=10 width=32 align=center class=migi>$yokoziku_koumoku</td>\n";
		}
		print "</tr>";
		
#==========ヨコの番号(td)の数だけタテの記号(tr)を出力==========#
		$i = 21;
		foreach $tateziku_kigou  (a..l) {
			print "<tr valign=center><td height=32 width=10 align=center class=sita>$tateziku_kigou</td>\n";
			foreach $yokoziku_bangou (1..16) {
				$name_seikei= "t_" . $tateziku_kigou . $yokoziku_bangou;
				print "<td height=32 width=32><input type=text size=4 value=\"$town_sprit_matrix[$yokoziku_bangou + $i]\" name=$name_seikei style=font-size:10px></td>\n";
			}
			print "</tr>\n";
			$i += 17;
		}
	print <<"EOM";
      </table>
	<br><div align=center><input type=submit value=" O K ">
	<a href=\"javascript:history.back()\"> [前の画面に戻る] </a>
	</div>
	</form>
	</td><td valign=top><!--テーブル右部分-->
	■パーツ＆記号対応表\<br>
	<FORM NAME="foMes5">
<INPUT TYPE="text" SIZE="82" NAME="TeMes5" style="font-size:10px; color:#000000; background-color:#d6dbbf"></FORM>
EOM
	&parts_taiou_hyou;
	print <<"EOM";
	</td></tr></table>
	</body></html>
EOM
}

#----------パーツ＆キーワード対応表----------#
sub parts_taiou_hyou {
	print <<"EOM";
	<table border="0" cellspacing="0" cellpadding="5" width=90% bgcolor=#ffffcc>
	<tr class=jouge bgcolor=#ffff99 align=center><td>記号</td><td>パーツ</td><td>記号</td><td>パーツ</td><td>記号</td><td>パーツ</td><td>記号</td><td>パーツ</td><td>記号</td><td>パーツ</td></tr><tr>
EOM

	@parts_keys = keys %unit;
	@parts_keys = sort {$a cmp $b} @parts_keys;
	
	$i = 1;
	foreach (@parts_keys){
		if ($_ ne "地"){
			print "<td align=right nowrap>$_</td>$unit{$_}";
			if ($i % 5 == 0){print "</tr><tr>";}
			$i ++;
		}
	}

	print <<"EOM";
	</tr>
	<tr><td colspan=8>
	</td></tr></table>
EOM
}

#----------管理者作成BBS----------#
sub admin_bbs {
	if ($in{'admin_pass'} ne $admin_pass2){&error("パスワードが違います");}
	&header;
	&bbs1_settei;
	&hooter_a2("admin","戻る","$this_script");
	exit;
}

#----------参加者一覧----------#
sub itiran {
	if ($in{'admin_pass'} ne $admin_pass2){&error("パスワードが違います");}
	&header;
	open(IN,"$logfile") || &error("Open Error : $logfile");
	eval{ flock (IN, 2); };
	@rankingMember = <IN>;
	close(IN);
	
	if($in{'sort_id'} eq ""){
		@keys0 = map {(split /<>/)[$in{'sort_id'}]} @rankingMember;
		@alldata = @rankingMember[sort {@keys0[$a] <=> @keys0[$b]} 0 .. $#keys0];
	}elsif($in{'sort_id'} eq "1" || $in{'sort_id'} eq "28"){
		@keys0 = map {(split /<>/)[$in{'sort_id'}]} @rankingMember;
		@alldata = @rankingMember[sort {@keys0[$a] cmp @keys0[$b]} 0 .. $#keys0];
	}else{
		@keys0 = map {(split /<>/)[$in{'sort_id'}]} @rankingMember;
		@alldata = @rankingMember[sort {@keys0[$b] <=> @keys0[$a]} 0 .. $#keys0];
	}
	
#==========同一ホストの配列を作成==========#
	if($in{'sort_id'} eq "28"){
			foreach (@alldata) {
				&list_sprit($_);
				if($list_host eq "$maeno_host"){
						push @tajuutouroku , $_;
						$check_flag=0;
						foreach $two(@tajuutouroku){
							(@check_list_host)= split(/<>/,$two);
									if($list_host eq "$check_list_host[28]"){$check_flag ++;}
						}
						if($check_flag <= 1 && $maeno_data ne ""){push @tajuutouroku , $maeno_data;}
				}
				$maeno_host = $list_host;
				$maeno_data = $_;
			}
	}

	print <<"EOM";
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="itiran">
	<input type=hidden name=command value="kozin_file">
	<input type=hidden name=kanrisya_id value="$in{'kanrisya_id'}">
	<input type=hidden name=admin_pass value="$in{'admin_pass'}">
禁止ホスト <input type=text name=host size="20">アクセス禁止にします。
EOM

	open(IN,"dene2.cgi") || &error("Open Error : dene2.cgi");
	eval{ flock (IN, 2); };
	@dene2 = <IN>;
	close(IN);
	if ($in{'host'}){
		unshift @dene2,"$in{'host'}\n";
	}
	print "<input type=\"radio\" name=\"kaijyo\" value=\"\">選択しない。\n";
	print "<input type=\"submit\" value=\"実行\"><br>\n";
	foreach $ado(@dene2){
		chomp $ado;
		if ($in{'kaijyo'} eq  $ado){
			$ado="";
			next;
		}

		print "<input type=\"radio\" name=\"kaijyo\" value=\"$ado\">$ado<br>\n";
		push @dene_2,"$ado\n";
	}
	open(IN,"> dene2.cgi") || &error("Open Error : dene2.cgi");
	eval{ flock (IN, 2); };
	print IN @dene_2;
	close(IN);
	print "</form>\n";
    
	$pag = int(($#alldata+1)/$ichi_page);
	if(($#alldata+1)%$ichi_page != 0){$pag++;}
	$i=0;
	foreach(1..$pag){
		$saki = $i*$ichi_page;
		$ato =($i+1)*$ichi_page-1;
		if($#alldata+1 < ($i+1)*$ichi_page){$ato = $#alldata;}
		$i++;
		if($stato_saki eq ""){
			$stato_saki = $saki;
			$stato_ato = $ato;
		}
		print "<a href=$this_script?mode=itiran&saki=$saki&ato=$ato&sort_id=$in{'sort_id'}&admin_pass=$in{'admin_pass'}>ページ$i</a> "; 
	}
	if($in{'saki'} ne ""){
		$saki = $in{'saki'};
		$ato = $in{'ato'};
	}else{
		$saki = $stato_saki;
		$ato = $stato_ato;
	}
	
	print <<"EOM";
	<br>
	<center>
	<table border=0 width=95% align=center cellspacing="1" cellpadding="5">
	<tr  class=jouge bgcolor=#ffff66><td align=center >ID</td><td align=center  width=120>名前</td><td align=center >性別</td><td align=center >資産</td><td align=center >職業</td><td align=center >最後の食事</td><td align=center >ホスト</td><td align=center >ブラックリスト</td></tr>
EOM

#==========多重登録者表示==========#
	if($in{'sort_id'} eq "28"){
		print "<tr  class=jouge bgcolor=#bbbbbb><td colspan=8>多重登録者（同一IP or ホストでの登録者）</td></tr>";
		foreach (@tajuutouroku) {
			&list_sprit($_);
			
#==========性別表示を整形==========#
	if ($list_sex eq "f") {$seibetu = "女";}else{$seibetu = "男";}
	
#==========最終食事表示を整形==========#
	$ENV{'TZ'} = "JST-9";
	($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime($list_last_syokuzi);
	my $mon  = $mon+1;
	my $year = $year + 1900;
	my $a_date = "$year年$mon月$mday日  $hour時$min分";

						print <<"EOM";
<tr class=sita2><td align=center>$list_k_id</td><td nowrap><a href=$this_script?mode=kensaku&command=kozin_file&k_id=$list_k_id&admin_pass=$in{'admin_pass'}>$list_name</a></td><td align=center>$seibetu</td><td align=right nowrap>$list_sousisan円</td><td>$list_job</td><td align=left nowrap>$a_date</td><td align=left nowrap>$list_host</td><td align=left nowrap>$list_k_yobi3</td></tr>
EOM
		}
		print "<tr  class=sita2 bgcolor=#ffffcc><td colspan=8>以下全参加者のリスト</td></tr>";
	}
	
	foreach (@alldata){
		&list_sprit($_);
		if ($list_sex eq "f") {$seibetu = "女";$f_count ++ ;}else{$seibetu = "男";$m_count ++ ;}
	}
	$i = $saki;
	foreach ($saki..$ato){
		&list_sprit($alldata[$i]);
		$i++;
		if ($list_sex eq "f") {$seibetu = "女";}else{$seibetu = "男";}
        
#==========最終食事表示を整形==========#
	$ENV{'TZ'} = "JST-9";
	($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime($list_last_syokuzi);
	my $mon  = $mon+1;
	my $year = $year + 1900;
	my $a_date = "$year年$mon月$mday日  $hour時$min分";
	
						print <<"EOM";
<tr class=sita2><td align=center>$list_k_id</td><td nowrap>$list_name</td><td align=center>$seibetu</td><td align=right nowrap>$list_sousisan円</td><td>$list_job</td><td align=left nowrap>$a_date</td><td align=left nowrap>$list_host</td><td align=left nowrap>$list_k_yobi3</td></tr>
EOM
		}
	close(IN);
	$total_count=$m_count+$f_count;
	print <<"EOM";
</table>
EOM
	&hooter_a2("admin","戻る","$this_script");
	exit;
}
sub kensaku {
	if ($in{'admin_pass'} ne $admin_pass2){&error("パスワードが違います");}
	
#==========名前クリックまたはID検索の場合==========#
	if ($in{'k_id'}){
		$kensaku_ID = "$in{'k_id'}";
		
#==========名前検索の場合==========#
	}elsif($in{'name'}){
			open(HUK,"$logfile") || &error("Open Error : $logfile");
			eval{ flock (HUK, 2); };
			$hukkatu_flag=0;
			while (<HUK>) {
					&kozin_sprit;
					if($in{'name'} eq $name){$hukkatu_flag=1; $kensaku_ID = "$k_id"; last;}
			}
			close(HUK);
			if($hukkatu_flag == 0){&error("$in{'name'}の名前で登録されている方はいません");}
	}else{&error("検索対象がわかりません");}
		
#==========個人ファイル検索の場合==========#
	if($in{'command'} eq "kozin_file"){
			$my_log_file = "./member/"."$kensaku_ID"."/log.cgi";
			$my_backlog_file = "./member/"."$kensaku_ID"."backup/backup_log.cgi";
			if (! -e $my_log_file){
				$backup_comment = "<br>ログファイルが存在しないためバックアップデータを開いています。データ復活ボタンを押してデータを復活させることができます。";
				$my_log_file = $my_backlog_file;
				if (! -e $my_backlog_file){&error("ID番号$kensaku_IDのログファイルは存在しません");}
			}
			
			open(MYL,"$my_log_file") || &error("ログファイル（$my_log_file）が開けません");
			eval{ flock (MYL, 2); };
			$my_prof = <MYL>;
			&kozin_sprit2($my_prof);
			close(MYL);
			$hukkatu_botan= <<"EOM";
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="deletUsr">
	<input type=hidden name=command value="del_kakunin">
	<input type=hidden name=name value="$name">
	<input type=hidden name="k_id" value="$kensaku_ID">
	<input type=hidden name=admin_pass value="$in{'admin_pass'}">
	<input type=submit value="このユーザーを削除する">
	</form>
EOM
			$page_comment = "$nameさんの個人ファイルデータです。$backup_comment";
			$data_syuusei_title =<<"EOM";
			<div class=honbun2>■データ修正</div>
	※入力欄がある項目はこちらでデータを変更することができます。ブラックリストに文字が記録されていてログインできない方のログインを許可をする場合は、ブラックリストの文字を消去してください。
EOM

#==========データ復活の場合==========#
	}elsif($in{'command'} eq "hukkatu"){
			$my_log_file = "./member/"."$kensaku_ID"."backup/backup_log.cgi";
			if (! -e $my_log_file){&error("ID番号$kensaku_IDのログファイルは存在しません");}
			open(MYL,"$my_log_file") || &error("ログファイル（$my_log_file）が開けません");
			eval{ flock (MYL, 2); };
			$my_prof = <MYL>;
			&kozin_sprit2($my_prof);
			close(MYL);
	
			$hukkatu_botan= <<"EOM";
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="hukkatu">
	<input type=hidden name="k_id" value="$kensaku_ID">
	<input type=hidden name=admin_pass value="$in{'admin_pass'}">
	<input type=submit value="このデータで復活させる">
	</form>
EOM
			$page_comment = "$nameさんのバックアップされているデータです。";
			$data_syuusei_title = "<div class=honbun2>■保存されているデータ</div>";
	}
		&header;

		#+++++性別表示を整形+++++#
	if ($sex eq "f") {$seibetu = "女";}else{$seibetu = "男";}
		#+++++最終食事表示を整形+++++#
	$ENV{'TZ'} = "JST-9";
	($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime($last_syokuzi);
	$mon  = $mon+1;
	$year = $year + 1900;
	$s_date = "$year/$mon/$mday  $hour : $min";
		#+++++アクセス日時を整形+++++#
	$ENV{'TZ'} = "JST-9";
	($a_sec,$a_min,$a_hour,$a_mday,$a_mon,$a_year,$a_wday) = localtime($access_byou);
	$a_mon  = $a_mon+1;
	$a_year = $a_year + 1900;
	$access_date = "$a_year/$a_mon/$a_mday  $a_hour : $a_min";
	
					print <<"EOM";
	<div align=center class=tyuu>$page_comment</div><br><br>
	<table width="95%" border="0" cellspacing="0" cellpadding="5" align=center style="font-size:11px" class=yosumi><tr><td>
			<form method="POST" action="$this_script">
			<input type=hidden name=mode value="kozindata_henkou">
			<input type=hidden name=admin_pass value="$in{'admin_pass'}">
			<input type=hidden name="k_id" value="$k_id">
			<input type=hidden name="name" value="$name">
	<table width="95%" border="0" cellspacing="0" cellpadding="3" align=center style="font-size:11px">
	<tr><td colspan=6>
	$data_syuusei_title
	</td></tr>
	<tr>
	<td>●名前<br>$name</td>
	<td>●性別<br><input type=text size=5 value="$seibetu" name=seibetu>※男 or 女</td>
	<td>●パスワード<br><input type=text size=16 value="$pass" name=pass></td>
	<td>●身長<br><input type=text size=5 value="$sintyou" name=sintyou>cm</td>
	<td>●体重<br><input type=text size=10 value="$taijuu" name=taijuu>kg</td>
	<td>●最終アクセス<br>$access_date</td></tr><tr>
	
	<td>●総資産<br>$k_sousisan円</td>
	<td>●持ち金<br><input type=text size=16 value="$money" name=money>円</td>
	<td>●銀行<br><input type=text size=16 value="$bank" name=bank>円</td>
	<td>●スーパー定期<br><input type=text size=16 value="$super_teiki" name=super_teiki>円</td>
	<td nowrap>●ローン日額<br><input type=text size=16 value="$loan_nitigaku" name=loan_nitigaku>円</td>
	<td>●ローン残回数<br><input type=text size=5 value="$loan_kaisuu" name=loan_kaisuu>回</td></tr><tr>
	
	<td>●最後の食事<br>$s_date</td>
	<td>●身体エネルギー<br><input type=text size=10 value="$energy" name=energy></td>
	<td>●頭脳エネルギー<br><input type=text size=10 value="$nou_energy" name=nou_energy></td>
	<td colspan=2>●ホスト<br>$host</td>
	<td>●ブラックリスト<br><input type=text size=20 value="$k_yobi3" name=k_yobi3></td></tr><tr>
	
	<td>●病気<br><input type=text size=20 value="$byoumei" name=byoumei></td>
	<td>●病気指数<br><input type=text size=20 value="$byouki_sisuu" name=byouki_sisuu></td>
	<td>●職業<br><input type=text size=24 value="$job" name=job></td>
	<td>●マスター職業<br><input type=text size=24 value="$jobsyu" name=jobsyu></td>
	<td>●仕事経験値<br><input type=text size=10 value="$job_keiken" name=job_keiken></td>
	<td>●勤務回数<br><input type=text size=10 value="$job_kaisuu" name=job_kaisuu>回</td></tr><tr>
	</table><br>
	
	<table width="95%" border="0" cellspacing="0" cellpadding="3" align=center><tr>
	<td>●国　　語 <input type=text size=6 value="$kokugo" name=kokugo></td>
	<td>●数　学 <input type=text size=6 value="$suugaku" name=suugaku></td>
	<td>●理　科 <input type=text size=6 value="$rika" name=rika></td>
	<td>●社　　会 <input type=text size=6 value="$syakai" name=syakai></td>
	<td>●英　語 <input type=text size=6 value="$eigo" name=eigo></td>
	<td>●音　楽 <input type=text size=6 value="$ongaku" name=ongaku></td>
	<td>●美　術 <input type=text size=6 value="$bijutu" name=bijutu></td></tr><tr>
	<td>●ルックス <input type=text size=6 value="$looks" name=looks></td>
	<td>●体　力 <input type=text size=6 value="$tairyoku" name=tairyoku></td>
	<td>●健　康 <input type=text size=6 value="$kenkou" name=kenkou></td>
	<td>●スピード <input type=text size=6 value="$speed" name=speed></td>
	<td>●パワー <input type=text size=6 value="$power" name=power></td>
	<td>●腕　力 <input type=text size=6 value="$wanryoku" name=wanryoku></td>
	<td>●脚　力 <input type=text size=6 value="$kyakuryoku" name=kyakuryoku></td></tr><tr>
	<td>●ＬＯＶＥ <input type=text size=6 value="$love" name=love></td>
	<td>●面白さ <input type=text size=6 value="$unique" name=unique></td>
	<td>●エッチ <input type=text size=6 value="$etti" name=etti></td>
	</tr></table>
EOM
	if($in{'command'} eq "kozin_file"){
		print "<div align=center><input type=submit value=\"データ修正\"></div>";
	}
	print <<"EOM";
	</td></tr></table></form>
	<br><br>
EOM
	if($in{'command'} eq "kozin_file"){
	print <<"EOM";
	<table width="95%" border="0" cellspacing="0" cellpadding="5" align=center style="font-size:11px" class=yosumi><tr><td colspan=2>
	<div class=honbun2>■振り込み</div>
	※任意のお金を振り込むことができます。振り込み者の名前は初期設定の「管理者名」になります。マイナスの金額を入力することで減金させることができます。
	</td></tr><tr><td width=220>
	$nameさんにお金を振り込む</td><td>
	<form method="POST" action="basic.cgi">
	<input type=hidden name=mode value="ginkoufurikomi">
	<input type=hidden name=command value="from_system">
	<input type=hidden name=name value="副管理人">
	<input type=hidden name=admin_pass value="$in{'admin_pass'}">
	<input type=hidden name=k_id value="$kensaku_ID">
	<input type=hidden name=aitenonamae value="$name">
	振り込み金額 <input type=text name=hurikomigaku size=12>円
	<input type=submit value="振り込み">
	</form>
	</td></tr></table>
	<br><br>
	<table width="95%" border="0" cellspacing="0" cellpadding="5" align=center style="font-size:11px" class=yosumi><tr><td width=300>
	<div class=honbun2>■メッセージ送信</div>
	※$nameさんにメッセージを送信することができます。送信者名は初期設定の「管理者名」になります。
	</td><td>
	<form method="POST" action="$script">
	<input type=hidden name=mode value="mail_do">
	<input type=hidden name=command value="from_system">
	<input type=hidden name=name value="副管理人">
	<input type=hidden name=admin_pass value="$in{'admin_pass'}">
	<input type=hidden name="sousinsaki_name" value="$name">
	<textarea cols=50 rows=4 name=m_com wrap="soft"></textarea>
	<input type="submit" value="メッセージ送信">
	</form></td></tr></table>
	<br><br>
	
<table width="95%" border="0" cellspacing="0" cellpadding="5" align=center style="font-size:11px" class=yosumi><tr><td width=300>
	<div class=honbun2>■バックアップデータの復活</div>
	※$nameさんの現行データを最後に保存されたデータに切り替えます。
	</td><td>
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="kensaku">
	<input type=hidden name=command value="hukkatu">
	<input type=hidden name=k_id value="$kensaku_ID">
	<input type=hidden name=admin_pass value="$in{'admin_pass'}">
	<input type=hidden name="hukkatu_name" value="$name">
	<input type="submit" value="データ復活">
	</form></td></tr></table>
	<br><br>
EOM
	}
	print <<"EOM"; 
	<div align=center>$hukkatu_botan
	<br><a href=\"javascript:history.back()\"> [前の画面に戻る] </a></div>
	</body></html>
EOM
exit;
}

#----------個人データ変更----------#
sub kozindata_henkou {
	if ($in{'admin_pass'} ne $admin_pass2){&error("パスワードが違います");}
	
#==========リストデータ修正==========#
	open(IN,"$logfile") || &error("Open Error : $logfile");
	eval{ flock (IN, 2); };
	@rankingMember = <IN>;
	close(IN);
		$sonzai_flag=0;
		if ($in{'seibetu'} eq "男"){$henkou_seibetu = "m";}elsif($in{'seibetu'} eq "女"){$henkou_seibetu = "f";}
		else{&error("性別は「男」か「女」にしてください");}
		foreach (@rankingMember) {
			&list_sprit($_);
			if ($list_name eq "$in{'name'}"){
				$sonzai_flag=1;
				$list_name = $in{'name'}; $list_sex = $henkou_seibetu; $list_pass = $in{'pass'};
				$list_sintyou = $in{'sintyou'}; $list_taijuu = $in{'taijuu'};
				$list_money = $in{'money'}; $list_bank = $in{'bank'}; $list_super_teiki = $in{'super_teiki'};
				$list_loan_nitigaku = $in{'loan_nitigaku'}; $list_loan_kaisuu = $in{'loan_kaisuu'}; $list_energy = $in{'energy'};
				$list_nou_energy = $in{'nou_energy'}; $list_k_yobi3 = $in{'k_yobi3'}; $list_byoumei = $in{'byoumei'};
				$list_byouki_sisuu = $in{'byouki_sisuu'}; $list_job = $in{'job'}; $list_jobsyu = $in{'jobsyu'};
				$list_job_keiken = $in{'job_keiken'}; $list_job_kaisuu = $in{'job_kaisuu'}; $list_kokugo = $in{'kokugo'};
				$list_suugaku = $in{'suugaku'}; $list_rika = $in{'rika'}; $list_syakai = $in{'syakai'};
				$list_eigo = $in{'eigo'}; $list_ongaku = $in{'ongaku'}; $list_bijutu = $in{'bijutu'};
				$list_looks = $in{'looks'}; $list_tairyoku = $in{'tairyoku'}; $list_kenkou = $in{'kenkou'};
				$list_speed = $in{'speed'}; $list_power = $in{'power'}; $list_wanryoku = $in{'wanryoku'}; $list_kyakuryoku = $in{'kyakuryoku'};
				$list_love = $in{'love'}; $list_unique = $in{'unique'}; $list_etti = $in{'etti'};
			}
			&list_temp;
			push (@new_ranking_data,$list_temp);
		}
		if ($sonzai_flag==0){&error("リストにその名前の参加者が見つかりません");}
	
#==========個人データ修正==========#
		$my_log_file = "./member/$in{'k_id'}/log.cgi";
		open(MYL,"$my_log_file")|| &error("Open Error : $my_log_file");
		eval{ flock (MYL, 2); };
		$my_prof = <MYL>;
		&kozin_sprit2($my_prof);
		close(MYL);
				$name = $in{'name'}; $sex = $henkou_seibetu; $pass = $in{'pass'};
				$sintyou = $in{'sintyou'}; $taijuu = $in{'taijuu'}; $sousisan = $in{'k_sousisan'};
				$money = $in{'money'}; $bank = $in{'bank'}; $super_teiki = $in{'super_teiki'};
				$loan_nitigaku = $in{'loan_nitigaku'}; $loan_kaisuu = $in{'loan_kaisuu'}; $energy = $in{'energy'};
				$nou_energy = $in{'nou_energy'}; $k_yobi3 = $in{'k_yobi3'}; $byoumei = $in{'byoumei'};
				$byouki_sisuu = $in{'byouki_sisuu'}; $job = $in{'job'}; $jobsyu = $in{'jobsyu'};
				$job_keiken = $in{'job_keiken'}; $job_kaisuu = $in{'job_kaisuu'}; $kokugo = $in{'kokugo'};
				$suugaku = $in{'suugaku'}; $rika = $in{'rika'}; $syakai = $in{'syakai'};
				$eigo = $in{'eigo'}; $ongaku = $in{'ongaku'}; $bijutu = $in{'bijutu'};
				$looks = $in{'looks'}; $tairyoku = $in{'tairyoku'}; $kenkou = $in{'kenkou'};
				$speed = $in{'speed'}; $power = $in{'power'}; $wanryoku = $in{'wanryoku'}; $kyakuryoku = $in{'kyakuryoku'};
				$love = $in{'love'}; $unique = $in{'unique'}; $etti = $in{'etti'};
		
	&temp_routin;
	&log_kousin($my_log_file,$k_temp);
	
	&lock;
	
	if ($mem_lock_num == 0){
		$err = data_save($logfile, @new_ranking_data);
		if ($err) {&error("$err");}
	}else{
		open(OUT,">$logfile") || &error("Write Error : $logfile");
		eval{ flock (OUT, 2); };
		print OUT @new_ranking_data;
		close(OUT);
	}

	&unlock;
	&message("データ修正をしました。","itiran","$this_script");
	&kensaku;
}

#----------ユーザー消す----------#
sub deletUsr {
	if ($in{'admin_pass'} ne $admin_pass2){&error("パスワードが違います");}
	if($in{'command'} eq "del_kakunin"){
			&header;
			print <<"EOM";
			<br><br><div align=center>$in{'name'}さんを削除します。よろしいですか？
			<form method="POST" action="$this_script">
			<input type=hidden name=mode value="deletUsr">
			<input type=hidden name=name value="$in{'name'}">
			<input type=hidden name="k_id" value="$in{'k_id'}">
			<input type=hidden name=admin_pass value="$in{'admin_pass'}">
			<input type=submit value="O K">
			</form>
			<a href=\"javascript:history.back()\"> [前の画面に戻る] </a>
			</div>
			</body></html>
EOM
			exit;
	}
	
	&lock;
	
#==========家削除処理==========#
					&ie_sakujo_syori ($in{'name'});
		#+++++フォルダー内のファイル名を取得して削除。個人フォルダーの削除+++++#
					use DirHandle;
					$dir = new DirHandle ("./member/"."$in{'k_id'}");
					while($file_name = $dir->read){
							unlink ("./member/$in{'k_id'}/$file_name");
					}
					$dir->close;
					rmdir("./member/$in{'k_id'}") || &error("memberディレクトリ内、$in{'k_id'}ディレクトリのデータ削除ができません");
		#+++++メンバーリストから削除+++++#
	open(IN,"$logfile") || &error("Open Error : $logfile");
	eval{ flock (IN, 2); };
	@rankingMember = <IN>;
		foreach (@rankingMember) {
			&list_sprit($_);
			if ($in{'k_id'} eq "$list_k_id"){next;}
			push @alldata,$_;
		}
		
#==========プロフィール＆結婚斡旋所削除処理==========#
	&prof_sakujo($in{'name'});
	&as_prof_sakujo($in{'name'});
	
	if ($mem_lock_num == 0){
		$err = data_save($logfile, @alldata);
		if ($err) {&error("$err");}
	}else{
		open(OUT,">$logfile") || &error("$logfileが開けません");
		eval{ flock (OUT, 2); };
		print OUT @alldata;
		close(OUT);
	}
	
	open(PROO,">$profile_file") || &error("$profile_fileに書き込めません");
	eval{ flock (PROO, 2); };
	print PROO @new_pro_alldata;
	close(PROO);
	
	open(ASPO,">$as_profile_file") || &error("$as_profile_fileに書き込めません");
	eval{ flock (ASPO, 2); };
	print ASPO @as_new_pro_alldata;
	close(ASPO);
	&unlock;

	&message("$in{'name'}さんを削除しました。","itiran","$this_script");
}


#----------データ復活----------#
sub hukkatu {
&lock;

#==========復活させるIDのフォルダが無い場合作成==========#
					$hukkatu_folder = "./member/$in{'k_id'}";
					if (! -e "$hukkatu_folder"){
						mkdir($hukkatu_folder, 0755) || &error("Error : can not Make Directry");
							if ($zidouseisei == 1){
								chmod 0777,"$hukkatu_folder";
							}elsif ($zidouseisei == 2){
								chmod 0755,"$hukkatu_folder";
							}else{
								chmod 0755,"$hukkatu_folder";
							}
					}

#==========フォルダー内のbackup_がついたファイル名を取得してバックアップデータを復活==========#
					use DirHandle;
					$back_folder_pass = "./member/"."$in{'k_id'}"."backup";
					$dir = new DirHandle ("$back_folder_pass");
					while($file_name = $dir->read){
							if($file_name =~ /^backup_/){
								open (BK,"$back_folder_pass/$file_name")  || &error("Open Error : ./member/$in{'k_id'}/$file_name");
								eval{ flock (BK, 2); };
								@back_data = <BK>;
								if ($file_name eq "backup_log.cgi"){@back_logdata = @back_data;}
								close (BK);
								$orig_file_name = substr ($file_name,7);
								open (BKO,">./member/$in{'k_id'}/$orig_file_name");
								eval{ flock (BKO, 2); };
								print BKO @back_data;
								close (BKO);
							}
					}
					$dir->close;
					@check_log = data_read($logfile);
					$list_aru_flag = 0;
					foreach (@check_log){
						&list_sprit($_);
						if($list_k_id eq "$in{'k_id'}"){$list_aru_flag = 1;last;}
					}
					
					if ($list_aru_flag == 0){
						push (@check_log,@back_logdata);
						if ($mem_lock_num == 0){
							$err = data_save($logfile, @check_log);
							if ($err) {&error("$err");}
						}else{
							open(CKO,">$logfile") || &error("Write Error : $logfile");
							eval{ flock (CKO, 2); };
							print CKO @check_log;
							close(CKO);
						}
					}
                    
					&unlock;
					&message("最後に保存したデータに切り替えました。","itiran","$this_script");
}


#----------管理者権限による卸商品更新----------#
sub ad_orosi_kousin {
	&lock;
	
#==========商品データログを開く==========#
	open(OL,"./dat_dir/syouhin.cgi") || &error("Open Error : ./dat_dir/syouhin.cgi");
	eval{ flock (OL, 2); };
	$top_koumoku = <OL>;
	
#==========商品をランダムに並び替えてログを更新==========#
	@new_syouhin_hairetu = ();
	srand ($$ | time);

	while (<OL>){
		my $r = rand @new_syouhin_hairetu+1;
		push (@new_syouhin_hairetu,$new_syouhin_hairetu[$r]);
		$new_syouhin_hairetu[$r] = $_;
	}
	close(OL);
	$i=0;
	foreach (@new_syouhin_hairetu){
		&syouhin_sprit($_);
		if ($syo_syubetu eq "食"){next;}
		if ($syo_syubetu eq 'デパート'){next;}
		$syo_zaiko = int ($syo_zaiko * $ton_zaiko_tyousei); 
		&syouhin_temp;
		push (@new_syouhin_hairetu2,$syo_temp);
		$i ++;
		if ($i >= $orosi_sinakazu){last;}
	}
	
#==========種別でソート==========#
	foreach (@new_syouhin_hairetu2){
		$data=$_;
		push @alldata,$data;
	}
	@keys1 = map {(split /<>/)[0]} @alldata;
	@alldata = @alldata[sort {$keys1[$a] cmp $keys1[$b]} 0 .. $#keys1];

	open(OLOUT,">$orosi_logfile") || &error("$orosi_logfileに書き込みが出来ません");
	eval{ flock (OLOUT, 2); };
	print OLOUT @alldata;
	close(OLOUT);
	
#==========更新日時を変更==========#
	open(IN,"$maintown_logfile") || &error("Open Error : $maintown_logfile");
	eval{ flock (IN, 2); };
	$maintown_para = <IN>;
	&main_town_sprit($maintown_para);
	close(IN);
	&time_get;
		#+++++卸フラグを１にしてメインタウンログを更新+++++#
	$mt_orosiflag = 1;
	$mt_yobi9 = $date2;
	&main_town_temp;
	open(OUT,">$maintown_logfile") || &error("Write Error : $maintown_logfile");
	eval{ flock (OUT, 2); };
	print OUT $mt_temp;
	close(OUT);	

	&unlock;
	&message("卸商品を更新しました。","admin","$this_script");
}

#----------デパート更新----------#
sub depaato_kousin{
	&time_get;
	$mt_syokudouflag=0;
	$mt_departflag=0;
	&main_town_temp;
	&lock;
	open(OUT,">$maintown_logfile") || &error("Write Error : $maintown_logfile");
	eval{ flock (OUT, 2); };
	print OUT $mt_temp;
	close(OUT);	
	&unlock;

	&message("デパート・食堂を更新します。","admin","$this_script");
}

#----------プロフィール削除----------#
sub prof_sakujo {
	open(PRO,"$profile_file") || &error("Open Error : $profile_file");
	eval{ flock (PRO, 2); };
	my @pro_alldata=<PRO>;
	close(PRO);
	@new_pro_alldata = ();
	foreach (@pro_alldata){
my ($pro_name,$pro_sex,$pro_age,$pro_addr,$pro_p1,$pro_p2,$pro_p3,$pro_p4,$pro_p5,$pro_p6,$pro_p7,$pro_p8,$pro_p9,$pro_p10,$pro_p11,$pro_p12,$pro_p13,$pro_p14,$pro_p15,$pro_p16,$pro_p17,$pro_p18,$pro_p19,$pro_p20)= split(/<>/);
			if (@_[0] eq "$pro_name"){next;} 
			push (@new_pro_alldata,$_);
	}
	
	open(PROO,">$profile_file") || &error("$profile_fileに書き込めません");
	eval{ flock (PROO, 2); };
	print PROO @new_pro_alldata;
	close(PROO);
}

#----------斡旋所プロフィール削除----------#
sub  as_prof_sakujo {
	open(ASP,"$as_profile_file") || &error("Open Error : $as_profile_file");
	eval{ flock (ASP, 2); };
	my @as_pro_alldata=<ASP>;
	close(ASP);
	@as_new_pro_alldata = ();
	foreach (@as_pro_alldata){
my ($pro_name,$pro_sex,$pro_age,$pro_addr,$pro_p1,$pro_p2,$pro_p3,$pro_p4,$pro_p5,$pro_p6,$pro_p7,$pro_p8,$pro_p9,$pro_p10,$pro_p11,$pro_p12,$pro_p13,$pro_p14,$pro_p15,$pro_p16,$pro_p17,$pro_p18,$pro_p19,$pro_p20)= split(/<>/);
			if (@_[0] eq "$pro_name"){next;} 
			push (@as_new_pro_alldata,$_);
	}
	
	open(ASPO,">$as_profile_file") || &error("$as_profile_fileに書き込めません");
	eval{ flock (ASPO, 2); };
	print ASPO @as_new_pro_alldata;
	close(ASPO);
}

#----------BBS1の設定----------#
sub bbs1_settei {

#==========管理者作成BBSの場合==========#
	if ($in{'mode'} eq "admin_bbs"){
			$my_directry = "./member/admin";
			if (! -d $my_directry){
						mkdir($my_directry, 0755) || &error("Error : can not Make Directry");
					if ($zidouseisei == 1){
						chmod 0777,"$my_directry";
					}elsif ($zidouseisei == 2){
						chmod 0755,"$my_directry";
					}else{
						chmod 0755,"$my_directry";
					}
			}
			$bbs1_settei_file="$my_directry/bbs".$in{'bbs_num'}."_ini.cgi";
			if (! -e $bbs1_settei_file){
				open(OIB,">$bbs1_settei_file") || &error("Write Error : $bbs1_settei_file");
				eval{ flock (OIB, 2); };
				chmod 0666,"$bbs1_settei_file";
				close(OIB);
			}
			$bbs1_log_file="$my_directry/bbs".$in{'bbs_num'}."_log.cgi";
			if (! -e $bbs1_log_file){
				open(OIL,">$bbs1_log_file") || &error("Write Error : $bbs1_log_file");
				eval{ flock (OIL, 2); };
				chmod 0666,"$bbs1_log_file";
				close(OIL);
			}
	}else{
			$my_directry = "./member/$in{'iesettei_id'}";
			$bbs1_settei_file="$my_directry/bbs1_ini.cgi";
			if (! -e $bbs1_settei_file){
				open(OIB,">$bbs1_settei_file") || &error("Write Error : $bbs1_settei_file");
				eval{ flock (OIB, 2); };
				chmod 0666,"$bbs1_settei_file";
				close(OIB);
			}
			$bbs1_log_file="$my_directry/bbs1_log.cgi";
			if (! -e $bbs1_log_file){
				open(OIL,">$bbs1_log_file") || &error("Write Error : $bbs1_log_file");
				eval{ flock (OIL, 2); };
				chmod 0666,"$bbs1_log_file";
				close(OIL);
			}
	}
		open(OIB,"$bbs1_settei_file") || &error("Open Error : $bbs1_settei_file");
		eval{ flock (OIB, 2); };
			$bbs1_settei_data = <OIB>;
			($bbs1_title,$bbs1_come,$bbs1_body_style,$bbs1_toukousya_style,$bbs1_table2_style,$bbs1_toukouwidth,$bbs1_a_hover_style,$bbs1_tablewidth,$bbs1_title_style,$bbs1_leed_style,$bbs1_siasenbako,$bbs1_yobi5,$bbs1_yobi6,$bbs1_yobi7,$bbs1_yobi8,$bbs1_yobi9,$bbs1_yobi10)= split(/<>/,$bbs1_settei_data);
#bbs1_yobi5 = 記事番号のスタイル　bbs1_yobi6＝同じ街の住民専用掲示板　bbs1_yobi7＝inputのスタイル
		close(OIB);
		

#==========スタイルの初期化==========#
	if ($bbs1_body_style eq ""){$bbs1_body_style = "background-color:#ffcc66;";}
	if ($bbs1_title_style eq ""){$bbs1_title_style = "font-size: 16px; color: #666666;line-height:180%; text-align:center;";}
	if ($bbs1_leed_style eq ""){$bbs1_leed_style = "font-size: 11px; line-height: 16px; color: #336699";}
	if ($bbs1_yobi5 eq ""){$bbs1_yobi5 = "font-size: 15px; color: #336699";}
	if ($bbs1_toukousya_style eq ""){$bbs1_toukousya_style = "font-size: 11px; color: #ff6600";}
	if ($bbs1_table2_style eq ""){$bbs1_table2_style = "font-size: 11px; line-height: 16px; color: #666666; background-color:#ffffcc; border: #336699; border-style: dotted; border-width:4px";}
	if ($bbs1_toukouwidth eq ""){$bbs1_toukouwidth = "50";}
	if ($bbs1_a_hover_style eq ""){$bbs1_a_hover_style = " color:#333333;text-decoration: none";}
	if ($bbs1_tablewidth eq ""){$bbs1_tablewidth = "500";}
	if ($bbs1_siasenbako eq ""){$bbs1_siasenbako = "font-size:11px;color:#000000";}
	if ($bbs1_yobi7 eq ""){$bbs1_yobi7 = "font-size:11px;color:#000000";}
	print <<"EOM";
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="bbs1_settei_do">
	<input type=hidden name=iesettei_id value="$in{'iesettei_id'}">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=admin_pass value="$in{'admin_pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value=$in{'town_no'}>
EOM
	if ($in{'mode'} eq "admin_bbs"){
	print "<input type=hidden name=bbs_num value=\"$in{'bbs_num'}\">\n";
	print "<input type=hidden name=command value=\"admin_bbs\">\n";
	}
	print <<"EOM";
	<table width="90%" border="0" cellspacing="0" cellpadding="8" align=center class=yosumi>
	<tr><td>
EOM
	if ($in{'mode'} eq "admin_bbs"){
		print "<div class=tyuu>■$admin_bbs_syurui[$in{'bbs_num'}]の掲示板設定</div>";
	}else{
		print "<div class=tyuu>■通常の掲示板設定</div>";
	}
	print <<"EOM";
	●掲示板のタイトル（タグ指定可。絶対URLならばイメージ画像の指定も可）<br>
	<textarea  cols=80 rows=4 name="タイトル" wrap="soft">$bbs1_title</textarea><br>
	●タイトル下のコメント<br>
	<input type=text name="コメント" size=120  value=$bbs1_come><br>
	●背景のスタイル設定<br>
	<input type=text name="bbs1_body_style" size=120 value="$bbs1_body_style"><br>
	●タイトルのスタイル設定<br>
	<input type=text name="bbs1_title_style" size=120 value="$bbs1_title_style"><br>
	●タイトル下のコメントのスタイル設定<br>
	<input type=text name="bbs1_leed_style" size=120 value="$bbs1_leed_style"><br>
	●記事番号のスタイル設定<br>
	<input type=text name="bbs1_yobi5" size=120 value="$bbs1_yobi5"><br>
	●投稿者名のスタイル設定<br>
	<input type=text name="bbs1_toukousya_style" size=120 value="$bbs1_toukousya_style"><br>
	●掲示板内の基本スタイル設定<br>
	<input type=text name="bbs1_table2_style" size=120 value="$bbs1_table2_style"><br>
	●投稿欄のサイズ（半角文字数で指定）<br>
	<input type=text name="bbs1_toukouwidth" size=120 value="$bbs1_toukouwidth"><br>
	●リンク（aタグ）のスタイル設定<br>
	<input type=text name="bbs1_a_hover_style" size=120 value="$bbs1_a_hover_style"><br>
	●テーブルの横幅<br>
	<input type=text name="bbs1_tablewidth" size=120 value="$bbs1_tablewidth"><br>
	●inputとselectのスタイル設定<br>
	<input type=text name="bbs1_siasenbako" size=120 value="$bbs1_siasenbako"><br>
	●レス部分のスタイル設定<br>
	<input type=text name="bbs1_yobi7" size=120 value="$bbs1_yobi7"><br>
EOM
	if ($in{'mode'} eq "admin_bbs"){
		print <<"EOM";
	●同じ街の住民専用掲示板にする（この掲示板を設置した街に住んでいる人だけが閲覧・書き込みできます）<br>
	<select name="bbs1_yobi6">
	<option value="">通常</option>
EOM
	if ($bbs1_yobi6 eq "on"){
		print "<option value=\"on\" selected>同じ街の住民専用</option>";
	}else{
		print "<option value=\"on\">同じ街の住民専用</option>"
	}
	print "</select><br><br>";
	}
	
	print "<input type=submit value=設定変更>";

		if ($in{'mode'} eq "admin_bbs"){
		print <<"EOM";
	<a href="original_house.cgi?mode=normal_bbs&ori_ie_id=admin&bbs_num=$in{'bbs_num'}&name=$in{'name'}&admin_pass=$in{'admin_pass'}&con_sele=0" target=_blank>[現在の設定内容の確認]</a>
	</td></tr></table>
	</form>
EOM
		}else{
		print <<"EOM";
	<a href="original_house.cgi?mode=houmon&ori_ie_id=$in{'iesettei_id'}&name=$in{'name'}&pass=$in{'pass'}&con_sele=0" target=_blank>[現在の設定内容の確認]</a>
	</td></tr></table>
	</form>
EOM
		}
}

#----------BBS1設定----------#
sub bbs1_settei_do {

#==========管理者作成BBSの場合==========#
	if ($in{'command'} eq "admin_bbs"){
		$bbs1_settei_file="./member/admin/bbs".$in{'bbs_num'}."_ini.cgi";
	}else{
		$bbs1_settei_file="./member/$in{'iesettei_id'}/bbs1_ini.cgi";
	}
		open(OIB,"$bbs1_settei_file") || &error("Open Error : $bbs1_settei_file");
		eval{ flock (OIB, 2); };
			$bbs1_settei_data = <OIB>;
			($bbs1_title,$bbs1_come,$bbs1_body_style,$bbs1_toukousya_style,$bbs1_table2_style,$bbs1_toukouwidth,$bbs1_a_hover_style,$bbs1_tablewidth,$bbs1_title_style,$bbs1_leed_style,$bbs1_siasenbako,$bbs1_yobi5,$bbs1_yobi6,$bbs1_yobi7,$bbs1_yobi8,$bbs1_yobi9,$bbs1_yobi10)= split(/<>/,$bbs1_settei_data);
		close(OIB);
		
		&lock;
			$bbs1_title = $in{'タイトル'};
			$bbs1_come = $in{'コメント'};
			$bbs1_body_style = $in{'bbs1_body_style'};
			$bbs1_toukousya_style = $in{'bbs1_toukousya_style'};
			$bbs1_table2_style = $in{'bbs1_table2_style'};
			$bbs1_toukouwidth = $in{'bbs1_toukouwidth'};
			$bbs1_a_hover_style = $in{'bbs1_a_hover_style'};
			$bbs1_tablewidth = $in{'bbs1_tablewidth'};
			$bbs1_title_style = $in{'bbs1_title_style'};
			$bbs1_leed_style = $in{'bbs1_leed_style'};
			$bbs1_siasenbako = $in{'bbs1_siasenbako'};
			$bbs1_yobi5 = $in{'bbs1_yobi5'};
			$bbs1_yobi6 = $in{'bbs1_yobi6'};
			$bbs1_yobi7 = $in{'bbs1_yobi7'};
			$bbs1_yobi8 = $in{'bbs1_yobi8'};
			$bbs1_yobi9 = $in{'bbs1_yobi9'};
			$bbs1_yobi10 = $in{'bbs1_yobi10'};
		$bbs_settei_temp = "$bbs1_title<>$bbs1_come<>$bbs1_body_style<>$bbs1_toukousya_style<>$bbs1_table2_style<>$bbs1_toukouwidth<>$bbs1_a_hover_style<>$bbs1_tablewidth<>$bbs1_title_style<>$bbs1_leed_style<>$bbs1_siasenbako<>$bbs1_yobi5<>$bbs1_yobi6<>$bbs1_yobi7<>$bbs1_yobi8<>$bbs1_yobi9<>$bbs1_yobi10<>\n";
	open(OLOUT,">$bbs1_settei_file") || &error("$bbs1_settei_fileに書き込みが出来ません");
	eval{ flock (OLOUT, 2); };
	print OLOUT $bbs_settei_temp;
	close(OLOUT);
		&unlock;
		if ($in{'command'} eq "admin_bbs"){
			&header;
	print <<"EOM";
	<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>設定を変更しました。</td></tr></table><br>
	
	<form method=POST action="$this_script">
	<input type=hidden name=mode value="admin_bbs">
	<input type=hidden name=name value=$in{'name'}>
	<input type=hidden name=pass value=$in{'pass'}>
	<input type=hidden name=admin_pass value=$in{'admin_pass'}>
	<input type=hidden name=bbs_num value=$in{'bbs_num'}>
	<input type=hidden name=town_no value=$in{'town_no'}>
	<input type=submit value="戻る">
	</form></div>
EOM
	exit;
		}else{
			&my_house_settei;
		}
}

#----------一斉メール----------#
sub mail_soshin {
	$member_f = './log_dir/memberlog.cgi';
	open(IN,"$logfile") || &error("Open Error : $logfile");
	eval{ flock (IN, 2); };
	@member = <IN>;
	close(IN);

	$kanrisyaname = "副管理人（$in{'name'}）";

	$in{'isseimail'} =~ s/<>/&lt;&gt;/g;

	&time_get;
	foreach (@member){
		(@member_list) = split(/<>/);
		$message_file = "./member/$member_list[0]/mail.cgi";
		unless(-e $message_file){next;}

		open(AIT,"$message_file") || &error("お相手の方のメール記録ファイル（$message_file）が開けません。");
		eval{ flock (AIT, 2); };
		$last_mail_check_time = <AIT>;
		@mail_cont = <AIT>;
		close(AIT);
		$new_mail = "受信<>$kanrisyaname<>$in{'isseimail'}<>$date2<>$date_sec<><><><><><>\n";
		unshift (@mail_cont,$new_mail);
		if (@mail_cont > $mail_hozon_gandosuu){pop @mail_cont;}


#==========最終メールチェック時間がなければ１を入れる==========#
		if ($last_mail_check_time eq ""){$last_mail_check_time = "1\n";}
		unshift (@mail_cont,$last_mail_check_time);
		open(OUT,">$message_file") || &error("$message_fileに書き込めません");
		eval{ flock (OUT, 2); };
		print OUT @mail_cont;
		close(OUT);
	}
	&header;
	print "<div align=center>\n";
	print "<br><br>以下の内容で送信完了しました。<br><br>\n";
	print "$in{'isseimail'}\n";
	print "<br><br><a href=\"javascript:history.back()\"> [前の画面に戻る] </a></div>\n";
	
	print "</body></html>\n";
	exit;
}

#----------専用フッター----------#
sub hooter_a2{
	print <<"EOM";
	<div align=center><form method=POST action="$_[2]">
	<input type=hidden name=mode value="$_[0]">
	<input type=hidden name=kanri value="fuku">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=admin_pass value="$in{'admin_pass'}">
	<input type=submit value="$_[1]">
	</form></div>
	</body></html>
EOM
}
