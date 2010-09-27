#!/usr/bin/perl

# ↑お使いのサーバーのパスに合わせてください。

#+++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2003-2004 brassiere
$version = 'TOWN ver.1.40';
#  web：http://brassiere.jp/
#  mail：shohei@brassiere.jp
#このプログラムによって起きた事に責任を負いません。
#+++++++++++++++++++++++++++++++++++++

###############################################################
# 紹介コードを表示するか
$syokai = 'yes';
# アイテムの数を表示
$kazu_disp = 'yes';
# タウンナンバーの保存
$hozontown = 'yes';
# プルダウンタウンページ　"no","yes","yes2","yes3":
$dairekutoin = 'no';
###############################################################

require './top.pl';
require './town_ini.cgi';
require './command.pl';
require './event.pl';
require './town_lib.pl';
require './unit.pl';
&decode;

# 指定ホストアクセス拒否
$get_host = $ENV{'REMOTE_HOST'};
$get_addr = $ENV{'REMOTE_ADDR'};
	
if ($get_host eq "" || $get_host eq $get_addr) {
	$get_host = gethostbyaddr(pack("C4", split(/\./, $get_addr)), 2) || $get_addr;
}

if ($get_host eq "") { &error("恐れ入りますがホストが取得できない環境ではアクセスできません"); }

if ($host_kyuka_meker eq 'yes'){
	if($okhost){
		local($flag)=1;
		foreach ( split(/\s+/, $okhost) ) {
			s/(\W)/\\$1/g;
			s/\*/\.\*/g;
			if ($get_host =~ /$_/) { $flag=0; last; }
		}
		if ($flag) { 
			$admin_pass = ''; 
		}
	}else{
		($host1,$host2,$host3,$host4) = split(/\./, $get_host);
		(@host5) = split(/\./, $get_host);
		$i = 0;
		foreach (@host5){
			if ($_ eq 'jp' || $_ eq 'JP' || $_ eq 'net'){
				$i++;
				if ($i >= 2){&error("host error $get_host");}
			}
		}

		(@kanri1) = split(/\./, $my_host1);
		if ($kanri1[0] eq '*'){
			$oboegaki1 = $host5[0];
			$host5[0] ='*';
			$get_host1 = join(".",@host5);
		}else{
			$get_host1 = $get_host;
		}
		
		$itti = "1";
		if ($my_host1 && $my_host1 eq $get_host1){
			$itti = "yes";
		}elsif($my_host1){
			$itti = "no";
		}
		
		if($oboegaki1){
			$host5[0] = $oboegaki1;
		}
		
		$get_host = join(".",@host5);
		(@kanri2) = split(/\./, $my_host2);
		if ($kanri2[0] eq '*'){
			$oboegaki2 = $host5[0];
			$host5[0] ='*';
			$get_host2 = join(".",@host5);
		}else{
			$get_host2 = $get_host;
		}
		
		if ($my_host2 && $my_host2 eq $get_host2 && ($itti eq "no" || $itti eq "1")){
			$itti = "yes";
		}elsif($my_host2){
			$itti = "no";
		}
		
		if ($itti eq "no"){
			$admin_pass = '';
		}
		
		if($oboegaki2){
			$host5[0] = $oboegaki2;
		}
		$get_host = join(".",@host5);
	}
}
#===================メンテチェック================
if($mente_flag == 1 && $in{'admin_pass'} eq "" && $in{'mode'} ne ""){&error("$mente_message")}

#===================よく分からない================
sub joukenbunki {}
	
#===================制限時間チェック==============
$seigenyou_now_time = time;
$ato_nanbyou=$koudou_seigen-($seigenyou_now_time - $access_byou);
if($seigenyou_now_time - $access_byou < $koudou_seigen){&error("まだ行動できません。あと$ato_nanbyou秒お待ちください。")}
		
#=================パスワードログ作成==============
if ( !-e $pass_logfile){
	open(LOGF,"< $logfile") || &error("Open Error : $logfile");
	eval{ flock (LOGF, 2); };
	@pass_sakuse = <LOGF>;
	close(LOGF);
	@henkan_pass = ();
	foreach (@pass_sakuse){
		&list_sprit($_);
		$henkan_temp = "$list_k_id<>$list_name<>$list_pass<>\n";
		push (@henkan_pass,$henkan_temp);
	}
	@henkan_pass = sort {$b <=> $a} @henkan_pass;

	open(PSS,">$pass_logfile") || &error("Write Error : $pass_logfile");
	eval{ flock (PSS, 2); };
	print PSS @henkan_pass;
	chmod 0666,"$pass_logfile";
	close(PSS);
}
	
#=================支払い方法==========================
if ($in{'mode'} eq "shiharaihouhou"){
	$shiharai = $in{'shiharai'};
	$in{'mode'} = "login_view";
}

#=================条件分岐==========================
if($in{'mode'} eq "login_view"){&login_view;}
if($in{'mode'} eq "orosi"){&orosi;}
if($in{'mode'} eq "buy_orosi"){&buy_orosi;}
if($in{'mode'} eq "syokudou"){&syokudou;}
if($in{'mode'} eq "syokuzisuru"){&syokuzisuru;}
if($in{'mode'} eq "syokudou2"){&syokudou2;}
if($in{'mode'} eq "syokuzisuru2"){&syokuzisuru2;}
if($in{'mode'} eq "depart_gamen"){&depart_gamen;}
if($in{'mode'} eq "depart_gamen2"){&depart_gamen2;}
if($in{'mode'} eq "buy_syouhin"){&buy_syouhin;}
if($in{'mode'} eq "buy_syouhin2"){&buy_syouhin2;}
if($in{'mode'} eq "hanbai"){&hanbai;}
if($in{'mode'} eq "buy_syouhin_hanbai"){&buy_syouhin_hanbai;}
if($in{'mode'} eq "kentiku"){&kentiku;}
if($in{'mode'} eq "kentiku_do"){&kentiku_do;}
if($in{'mode'} eq "aisatu"){&aisatu;}
if($in{'mode'} eq "mail_sousin"){&mail_sousin;}
if($in{'mode'} eq "mail_do"){&mail_do;}
if($in{'mode'} eq "jamp_url"){&jamp_url;}

if($sanka_flag==0 && $in{'town_no'} eq ""){
	$in{'town_no'}=int(rand(@town_hairetu));
}
&main_view($in{'town_no'});

exit;

####################################################
#/////////////////以下サブルーチン/////////////////#
####################################################


#---------------ログイン画面-------------------#
sub login_view {

#==========日付けが変わっていた場合のイベント=============
	&time_get;
	my ($hutuu_risoku,$teiki_risoku);
	if ($access_time ne "$date"){
		$access_time = $date;
		#+++++++++預金の利息計算++++++++++
		$hutuu_risoku = int ($bank*0.005);
		if ($hutuu_risoku > 0){
			$bank += $hutuu_risoku;
			&kityou_syori("普通預金利息","",$hutuu_risoku,$bank,"普");
		}
		$teiki_risoku = int ($super_teiki*0.01);
		if ($teiki_risoku > 0){
			$super_teiki += $teiki_risoku;
			&kityou_syori("スーパー定期利息","",$teiki_risoku,$super_teiki,"定");
		}
		#+++++++++住宅ローン引き落とし++++++++++
		if ($loan_kaisuu > 0){
			$bank -= $loan_nitigaku;
			$loan_kaisuu --;
			&kityou_syori("住宅ローン支払い","$loan_nitigaku","",$bank,"普");
		}
		#+++++++++税金徴収++++++++++
		if($zeikin_shitei){
			local($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime;#time
			@week = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
			if($zeikin_shitei =~ /[0-9]/){
				if($mday == $zeikin_shitei){
					$cyousyu = 1;
				}
			}elsif($week[$wday] eq $zeikin_shitei){
				$cyousyu = 1;
			}
			if($cyousyu){
				if ($k_sousisan <= 1000000){
					$hiku_kane = 0;
					$nouzeinashi =1;
				}elsif($k_sousisan <= 10000000){
					$zeiritu = '1';
					$hiku_kane = int($k_sousisan *0.01);
				}elsif($k_sousisan <= 100000000){
					$zeiritu = '3';
					$hiku_kane = int($k_sousisan *0.03);
				}elsif($k_sousisan <= 1000000000){
					$zeiritu = '5';
					$hiku_kane = int($k_sousisan *0.05);
				}else{
					$zeiritu = '7';
					$hiku_kane = int($k_sousisan *0.07);
				}
				$koukengen="1";
				if($kpoint < 25){
				   $koukengen="";
				}elsif($kpoint < 50){
				   $hiku_kane -= int($hiku_kane / 4);
				   $zeiritu -= int($zeiritu / 4);
				}elsif($kpoint < 100){
				   $hiku_kane -= int($hiku_kane / 3);
				   $zeiritu -= int($zeiritu / 3);
				}elsif($kpoint < 250){
				   $hiku_kane = int($hiku_kane / 2);
				   $zeiritu = int($zeiritu / 2);
				}elsif($kpoint < 500){
				   $hiku_kane = int($hiku_kane / 3);
				   $zeiritu = int($zeiritu / 3);
				}elsif($kpoint < 1000){
				   $hiku_kane = int($hiku_kane / 4);
				   $zeiritu = int($zeiritu / 4);
				}else{
				   $hiku_kane = 0;
				   $zeiritu = 0;
				}
				if($koukengen){$menzei="（Ｋポイント割引）";}
				if(!$nouzeinashi){
					$bank -= $hiku_kane;
					&kityou_syori("納税 $zeiritu %  $menzei","$hiku_kane","",$bank,"普");
				}
			}
		}

		#+++++++++子供からの仕送り処理++++++++++
		&kodomo_siokuri;
		&unei_siokuri2;
		&unei_siokuri3;
	}
	
#==========事故だった場合=============
	if ($in{'ziko_flag'} eq "on" && $in{'ziko_idousyudan'} ne "徒歩"){
		$monokiroku_file="./member/$k_id/mono.cgi";
		open(OUT,"< $monokiroku_file") || &error("Open Error : $monokiroku_file");
		eval{ flock (OUT, 2); };
		@mycar_hairetu = <OUT>;
		close(OUT);
		$ziko_sya_flg=0;
		@new_mycar_hairetu =();
		foreach  (@mycar_hairetu) {
			&syouhin_sprit($_);
			if ($syo_syubetu ne  "ギフト" && $syo_taikyuu > 0 && $in{'ziko_idousyudan'} eq "$syo_hinmoku" && $ziko_sya_flg == 0){
				$syo_taikyuu -- ;
				$ziko_sya_flg=1;
				if ($syo_taikyuu <= 0){
					$taiha_comment = "$in{'ziko_idousyudan'}は大破しました。";
				}else{
					$taiha_comment = "残りの耐久（$syo_taikyuu）";
				}
			}
			&syouhin_temp;
			push (@new_mycar_hairetu,$syo_temp);
		}
		
		#+++++++++自分の所有物ファイルを更新++++++++++
		&lock;
		open(OUT,">$monokiroku_file") || &error("Write Error : $monokiroku_file");
		eval{ flock (OUT, 2); };
		print OUT @new_mycar_hairetu;
		close(OUT);
		$loop_count = 0;
		while ($loop_count <= 10){
			for (0..50){$i=0;}
			@f_stat_b = stat($monokiroku_file);
			$size_f = $f_stat_b[7];
			if ($size_f == 0 && @new_mycar_hairetu ne ""){
				open (OUT, "> $monokiroku_file") or &error("エラー・ファイルが開けません $monokiroku_file");
				eval{ flock (OUT, 2); };
				print OUT @new_mycar_hairetu;
				close (OUT);
			}else{
				last;
			}
			$loop_count++;
		}
		
	if ($in{'maigo'} eq 'yes'){
	    $no_rand=int(rand(4));
		$in{'town_no'} = $no_rand;
		$disp = "<br>おまけに迷子になってしまいました。<br>$town_hairetu[$in{'town_no'}]に行ってしまいました。";
	}
	&unlock;
	&message("<font color=#ff6600>交通事故を起こしてしまいました！<br>「$in{'ziko_idousyudan'}」の耐久度が１減ります。<br>$taiha_comment$disp</font>","login_view");
	}

#==========迷子だった場合=============
	if ($in{'maigo'} eq 'yes'){
	    $no_rand=int(rand(4));
		&message("<font color=#ff6600>迷子になりました。<br>$town_hairetu[$in{'town_no'}]に行ってしまいました。</font>","login_view");
	}

	&event_happen;
	$k_sousisan = $money + $bank + $super_teiki - ($loan_nitigaku * $loan_kaisuu);
	if($sanka_flag==0 && $in{'town_no'} eq ""){
		$in{'town_no'}=int(rand(@town_hairetu));
	}
	&main_view("$in{'town_no'}");
	
exit;
}


#---------------トップ画面右部分-------------------#
sub top_gamen {
	open(IN,"< $maintown_logfile") || &error("Open Error : $maintown_logfile");
	eval{ flock (IN, 2); };
			$maintown_para = <IN>;
			if ($maintown_para eq ""){&error("$maintown_logfileに問題があります。お手数ですが管理人（$master_ad）までご連絡ください。");}
			
#==========空ログチェック=============
			&main_town_sprit($maintown_para);
	close(IN);
	&time_get;
	
#==========日付が変わっていたらメインタウンログを今日の日付に更新、卸時刻、明日の卸時刻を更新、卸フラグと食堂フラグを0にする=============
	if($date ne $mt_today){
			$mt_today=$date;
			$mt_t_time=$mt_y_time;
			$mt_y_time=int(rand(20))+1;
			$mt_orosiflag=0;
			$mt_syokudouflag=0;
			$mt_departflag=0;
			&main_town_temp;
			&lock;
			open(OUT,">$maintown_logfile") || &error("Write Error : $maintown_logfile");
			eval{ flock (OUT, 2); };
			print OUT $mt_temp;
			close(OUT);	
			&list_log_backup;
			&unlock;
	}

#==========右部分表示=============
	open(IN,"< $logfile") || &error("Open Error : $logfile");
	eval{ flock (IN, 2); };
	@rankingMember = <IN>;
	$sankasyasuu = @rankingMember;
			$men=0;
			$women=0;
		foreach (@rankingMember){
			&list_sprit($_);
			if($list_sex eq "m"){$men++;}
			else{$women++;}
		}
	close(IN);
	my $mt_keizai_hyouzi = int ($mt_keizai / (int(($date_sec - $mt_yobi8) / (60*60*24))+1));
	my $mt_henei_hyouzi = int ($mt_hanei / (int(($date_sec - $mt_yobi8) / (60*60*24))+1));
	
		#+++++++++上のほう++++++++++
	print <<"EOM";
      <table width="100%" border="0" cellspacing="0" cellpadding="3">
        <tr>
          <td colspan="3">
           <div align="center"><font size="5"><b>$title</b></font></div>
          </td>
        </tr>
        <tr class="yosumi">
          <td width="30%"><span onMouseOver="Navi('img/about.gif', '人口', '男：$men人、女：$women人', 1, event);" onMouseOut="NaviClose();">人口：$sankasyasuu人</td>
          <td width="30%"><span onMouseOver="Navi('img/about.gif', '経済力とは', '住民のお店の平均１日売り上げ額（街全体）', 1, event);" onMouseOut="NaviClose();">経済力：$mt_keizai_hyouzi円</span></td>
          <td width="30%"><span onMouseOver="Navi('img/about.gif', '繁栄度とは', '掲示板の平均１日書き込み数（街全体）', 1, event);" onMouseOut="NaviClose();">繁栄度：$mt_henei_hyouzi</span></td>
        </tr>
        <tr>
          <td colspan="3" bgcolor="#eeeeee">$osirase</td>
        </tr>
          <td colspan="3">
EOM

		#+++++++++ログイン人数が多いとき、違うとき++++++++++
	if ($genzaino_ninzuu >= $douzi_login_ninzuu){
		print "<div align=center><br><table  border=0  cellspacing=\"5\" cellpadding=\"0\" width=300 style=\"$message_win\"><tr><td>現在、同時ログイン制限$douzi_login_ninzuu人を超えています。恐れ入りますが、しばらくしてからログインしてください。</td></tr></table>";
	}else{
		if($hozontown eq 'yes'){$disp_tag = "<input type=\"hidden\" name=\"town_no\" value=\"$ck{'town_no'}\">\n";}else{$disp_tag="";}
	}
		
		#+++++++++ログインフォーム++++++++++
		print <<"EOM";
<br>
<Script Language="JavaScript">
<!--
function bzc(){
	document.getoin.burauza_in.value = navigator.appName;
}
//-->
</Script>
<table width="100%" border="3" bordercolor="#199eff" cellspacing="0" cellpadding="5">
<form method="POST" name="getoin" action="$script">
<input type=hidden name="mode" value="login_view">
<input type="hidden" name="burauza_in" value="">
<tr bgcolor="#199eff">
<td><font color="#ffffff">●ログイン（登録済みの方）</font></td>
</tr>
<tr bgcolor="#ffffff">
<td align="left">
	$disp_tag
	名　　　前　<input type="text" name="name" value="$ck{'name'}" size="20"><br>
	パスワード　<input type="text" name="pass" value="$ck{'pass'}" size="20"><br>
	一覧で名前を
	<select name="sanka_hyouzi_on">
	<option value="on" selected>表\示する</option>
	<option value="off">表\示しない</option>
	</select><br>
	<div align="center"><input type="submit" value="街に入る" onMouseDown='bzc()'></div>
</td>
</tr>
</form>
</table>
EOM

		#+++++++++新規登録フォーム++++++++++
	if ($sankasyasuu >= $saidai_ninzuu){
		print "※現在、最大登録人数に達していますので新規登録はできません。";
	}elsif($new_touroku_per == 1) {
		print <<"EOM";
<font color="red">
近畿地方のβ版が公開されました！！！<br>
次からは、こちらに登録してください！<br>
<a href="http://tyage.sakura.ne.jp/town/">http://tyage.sakura.ne.jp/town/</a>
</font>
EOM
	}else{
		print <<"EOM";
<br>
<table width="100%" border="3" bordercolor="#199eff" cellspacing="0" cellpadding="5">
<form method="POST" action="game.cgi">
<input type=hidden name=mode value="new_hyouji">
<tr bgcolor="#199eff">
<td><font color="#ffffff">●新規登録（最大登録人数：$saidai_ninzuu人）</font></td>
</tr>
<tr bgcolor="#ffffff">
<td align="center">
	<input type="submit" value="新規登録する">
</td>
</tr>
</form>
</table>
EOM
	}

		#+++++++++管理メニュー++++++++++
	print <<"EOM";
<br>
<table width="100%" border="3" bordercolor="#199eff" cellspacing="0" cellpadding="5">
<form method=POST action="admin2.cgi">
<input type=hidden name=mode value="admin">
<input type=hidden name=name value="$ck{'name'}">
<input type=hidden name=kanri value="fuku">
<tr>
<td bgcolor="#199eff" colspan="2"><font color="#ffffff">●副管理人用</font></td>
</tr>
<tr bgcolor="#ffffff">
<td align="left">
	パスワード　<input type="password" size="20" name="admin_pass"><br>
	<div align="center"><input type=submit value="副管理人入る"></div>
</td>
</tr>
</form>
</table>
<br>
<table width="100%" border="3" bordercolor="#199eff" cellspacing="0" cellpadding="5">
<form method=POST action="admin.cgi">
<input type=hidden name=mode value="admin">
<tr>
<td bgcolor="#199eff"><font color="#ffffff">●管理者（チャゲ）用</font></td>
</tr>
<tr bgcolor="#ffffff">
<td align="left">
	管理者ＩＤ　<input type="text" size="20" name="kanrisya_id"><br>
	パスワード　<input type="text" size="20" name="admin_pass"><br>
	<div align="center"><input type=submit value="管理人入る"></div>
</td>
</tr>
</form>
</table>

<br>
<a href="http://www.scalable.jp/?cid=220002"><img src="http://www.scalable.jp/images/banner/120x60.gif" alt="VPSレンタルサーバー" border="0"></a>

</td>
</tr>
</table>
EOM

}

#---------------街情報窓の出力-------------------#
sub town_jouhou {
	$keizai_hyouzi = int ($keizai / (int(($date_sec - $t_yobi2) / (60*60*24))+1));
	$hanei_hyouzi = int ($hanei / (int(($date_sec - $t_yobi2) / (60*60*24))+1));
	print <<"EOM";
<table width="100%" border="0" cellspacing="0" cellpadding="2" align=center class="yosumi"><tr><td>
<div align=center>
<span  class="tyuu">「$title」内</span><br>
<span  class="midasi">$town_name</span>
</div></td><td>
          <span onMouseOver="Navi('img/about.gif', '地　価とは', 'この街の土地の価格で、家の建設時に払わないといけません。', 1, event);" onMouseOut="NaviClose();">地　価：$town_tika_hairetu[@_[0]]万円</span><br>
          <span onMouseOver="Navi('img/about.gif', '経済力とは', 'この街の住民のお店の平均１日売り上げ額', 1, event);" onMouseOut="NaviClose();">経済力：$keizai_hyouzi円</span><br>
          <span onMouseOver="Navi('img/about.gif', '繁栄度とは', 'この街にある掲示板の平均１日書き込み数', 1, event);" onMouseOut="NaviClose();">繁栄度：$hanei_hyouzi</span>
</td></tr></table>
<br>
EOM
}

#---------------コマンドボタンの出力-------------------#
sub command_botan {
#==========購入物ファイルを開く=============
	$monokiroku_file="./member/$k_id/mono.cgi";
	if (! -e $monokiroku_file){
		open (OUT,">$monokiroku_file") || &error("自分の購入物ファイルを作成できません");
		eval{ flock (OUT, 2); };
		close(OUT);
	}
	open(OUT,"< $monokiroku_file") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 2); };
	@my_kounyuu_list =<OUT>;
	@mono_name_keys = ();
	@mono_kouka_keys = ();
	foreach (@my_kounyuu_list){
		&syouhin_sprit($_);
		if ($syo_taikyuu <= 0){next;}
		push (@mono_name_keys ,$syo_hinmoku);
		push (@mono_kouka_keys ,$syo_kouka);
	}
	$botanyou_mono_check = join("<>",@mono_name_keys);
	$botanyou_kouka_check = join("<>",@mono_kouka_keys);
	close(OUT);
	

#==========コマンドボタン=============

	if ($renai_system_on == 1){$botan_narabi_suu = 6;}else{$botan_narabi_suu = 5;}
	
	if ($in{'mysec'}){
		($sec_dis,$min_dis,$hour_dis,$mday_dis,$mon_dis,$year_dis,) = localtime($in{'mysec'} + 60*$work_seigen_time);
	}else{
		($sec_dis,$min_dis,$hour_dis,$mday_dis,$mon_dis,$year_dis,) = localtime($house_name + 60*$work_seigen_time);
	}
	$year_dis += 1900;
	$mon_dis++;
	if ($min_dis < 10){$min_dis = '0'.$min_dis}
	if ($sec_dis < 10){$sec_dis = '0'.$sec_dis}

	$kaigyou_flag=1;
	$top_botan  .= <<"EOM";
<form method=POST name=ct action="$script"><td><input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>login_view<>"><input type=hidden name=std value='$year_dis $mon_dis $mday_dis $hour_dis $min_dis $sec_dis'><input type=image src='$img_dir/button/reload.png' onMouseOver="Navi('$img_dir/button/reload.png', '画面更新', '画面を更新します。<br>「パワー」は休息後、このボタンを押すことで徐々に増えます。', 1, event);" onMouseOut="NaviClose();"></td></form>
EOM

	if ($job ne "学生"){
	$kaigyou_flag ++;
	if($kaigyou_flag % $botan_narabi_suu == 0){$top_botan  .=  "</tr><tr>";}

	$top_botan  .= <<"EOM";
<form method=POST name=ctw action="basic.cgi"><td><INPUT TYPE=hidden NAME="mysec"><input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>do_work<>"><input type=hidden name=cond value="$condition"><div id="comm"><input type=image src='$img_dir/button/go_work.png' onMouseOver="Navi('$img_dir/button/go_work.png', '仕事', '仕事に出かけます。<br>経験値：$job_keiken　勤務数：$job_kaisuu回', 1, event);" onMouseOut='NaviClose();'></div></td></form>
EOM
	}

	$kaigyou_flag ++;
	if($kaigyou_flag % $botan_narabi_suu == 0){$top_botan  .=  "</tr><tr>";}
	$top_botan  .= <<"EOM";
<form method=POST action="basic.cgi"><td><input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>item<>"><input type=image src='$img_dir/button/item.png' onMouseOver="Navi('$img_dir/button/item.png', 'アイテム', 'アイテムを使用します。<br>売却もできます。', 1, event);" onMouseOut="NaviClose();"></td></form>
EOM

	$kaigyou_flag ++;
	if($kaigyou_flag % $botan_narabi_suu == 0){$top_botan  .=  "</tr><tr>";}
	$top_botan  .= <<"EOM";
<form method=POST action="$script"><td><input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>mail_sousin<>"><input type=image src='$img_dir/button/mail.png' onMouseOver="Navi('$img_dir/button/mail.png', 'メッセージ', '街の住人あてにメッセージを送信することができます。<br>ギフトの送信、独自タグの使用ができます。', 1, event);" onMouseOut="NaviClose();"></td></form>
EOM

	$kaigyou_flag ++;
	if($kaigyou_flag % $botan_narabi_suu == 0){$top_botan  .=  "</tr><tr>";}
	$top_botan  .= <<"EOM";
<form method=POST action="game.cgi"><td><input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>battle<>"><input type=image src='$img_dir/button/battle.png' onMouseOver="Navi('$img_dir/button/battle.png', 'ストリートファイト', 'ストリートファイトに出かけます。<br>ほかの住民と戦います。', 1, event);" onMouseOut="NaviClose();"></td></form>
EOM

	$kaigyou_flag ++;
	if($kaigyou_flag % $botan_narabi_suu == 0){$top_botan  .=  "</tr><tr>";}
	if ($unit{$k_id} ne "" or $unit{$k_id."_0"} ne "" or $unit{$k_id."_1"} ne "" or $unit{$k_id."_2"} ne "" or $unit{$k_id."_3"} ne ""){
	$top_botan  .= <<"EOM";
<form method=POST action="original_house.cgi"><td><input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>my_house_settei<>"><input type=hidden name=iesettei_id value="$k_id"><input type=image src='$img_dir/button/my_housein.png' onMouseOver="Navi('$img_dir/button/my_housein.png', '自分の家', '自分の家に関する各種設定を行えます。<br>仕入れなどもできます。', 1, event);" onMouseOut="NaviClose();"></td></form>
EOM
	}

	$kaigyou_flag ++;
	if($kaigyou_flag % $botan_narabi_suu == 0){$top_botan  .=  "</tr><tr>";}
	if ($unit{$house_type} ne ""){
	$top_botan  .= <<"EOM";
<form method=POST action="original_house.cgi"><td><input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>my_house_settei<>"><input type=hidden name=iesettei_id value="$house_type"><input type=image src='$img_dir/button/my_housein2.png' onMouseOver="Navi('$img_dir/button/my_housein2.png', '配偶者の家', '配偶者の家に関する各種設定を行えます。<br>仕入れなどもできます。', 1, event);" onMouseOut="NaviClose();"></td></form>
EOM
	}
	
	$kaigyou_flag ++;
	if($kaigyou_flag % $botan_narabi_suu == 0){$top_botan  .=  "</tr><tr>";}
	if ($love >= $need_love && $renai_system_on == 1){
	$top_botan  .= <<"EOM";
<form method=POST action="kekkon.cgi"><td><input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>renai<>"><input type=image src='$img_dir/button/renai.png' onMouseOver="Navi('$img_dir/button/renai.png', '恋人', '恋人とデートをしたり、プロポーズしたりできます。<br>子供ができることもあります。', 1, event);" onMouseOut="NaviClose();"></td></form>
EOM
	}
	
	$kaigyou_flag ++;
	if($kaigyou_flag % $botan_narabi_suu == 0){$top_botan  .=  "</tr><tr>";}
	if ($love >= $need_love && $renai_system_on == 1){
	$top_botan  .= <<"EOM";
<form method=POST action="kekkon.cgi"><td><input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>kosodate<>"><input type=image src='$img_dir/button/kosodate.png' onMouseOver="Navi('$img_dir/button/kosodate.png', '子育て', '子育てをします。<br>子供は自立後に仕送りをしてくれます。', 1, event);" onMouseOut="NaviClose();"></td></form>
EOM
	}
	
	$kaigyou_flag ++;
	if($kaigyou_flag % $botan_narabi_suu == 0){$top_botan  .=  "</tr><tr>";}
	$top_botan  .= <<"EOM";
<form method=POST action="setup.cgi"><td><input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>setup<>"><input type=image src='$img_dir/button/setup.png' onMouseOver="Navi('$img_dir/button/setup.png', '設定', '自分のデータの設定を行えます。<br>また、死亡届をだしたり、メモ帳機能\を使ったりできます。', 1, event);" onMouseOut="NaviClose();"></td></form>
EOM

	$kaigyou_flag ++;
	if($kaigyou_flag % $botan_narabi_suu == 0){$top_botan  .=  "</tr><tr>";}
	$top_botan  .= <<"EOM";
<form method=POST action="game.cgi"><td><input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>data_hozon<>"><input type=image src='$img_dir/button/off.png' onMouseOver="Navi('$img_dir/button/off.png', '保存', 'データを保存します。<br>最後に保存した食事時間が$deleteUser日を超えるとユーザー削除されます。', 1, event);" onMouseOut="NaviClose();"></td></form>
EOM

}

#---------------個人パラメータ出力-------------------#
sub loged_gamen {

#==========パワーのMAX値計算=============
	$energy_max = int(($looks/12) + ($tairyoku/4) + ($kenkou/4) + ($speed/8) + ($power/8) + ($wanryoku/8) + ($kyakuryoku/8));
	$nou_energy_max = int(($kokugo/6) + ($suugaku/6) + ($rika/6) + ($syakai/6) + ($eigo/6)+ ($ongaku/6)+ ($bijutu/6));
	my ($date_sec) = time;
    
	if($energy_max >= $nou_energy_max){
		$tokubetu_times = int($energy_max / 50);
		if($tokubetu_times < 2){$tokubetu_times = 2;}
	}else{
		$tokubetu_times = int($nou_energy_max / 50);
		if($tokubetu_times < 2){$tokubetu_times = 2;}
	}
	
#==========身体パワー計算=============
	if ($in{'iiyudane'} eq "one"){
		$energy = $energy + int(($date_sec - $last_ene_time)/$sintai_kaihuku*$onsen_times);
	}elsif($in{'iiyudane'} eq "two"){
		$energy = $energy + int(($date_sec - $last_ene_time)/$sintai_kaihuku*$tokubetu_times);
	}elsif($in{'iiyudane'} eq "five"){
		$energy = $energy + int(($date_sec - $last_ene_time)/$sintai_kaihuku*$matu_times);
	}elsif($in{'iiyudane'} eq "fo"){ #take
		$energy = $energy + int(($date_sec - $last_ene_time)/$sintai_kaihuku*$take_times);
	}elsif($in{'iiyudane'} eq "three"){
		$energy = $energy + int(($date_sec - $last_ene_time)/$sintai_kaihuku*$ume_times);
	}elsif($in{'iiyudane'} eq "six"){
		$energy = $energy + int(($date_sec - $last_ene_time)/$sintai_kaihuku*$dou_times);
	}elsif($in{'iiyudane'} eq "seven"){
		$energy = $energy + int(($date_sec - $last_ene_time)/$sintai_kaihuku*$gin_times);
	}elsif($in{'iiyudane'} eq "eight"){
		$energy = $energy + int(($date_sec - $last_ene_time)/$sintai_kaihuku*$kin_times);
	}else{
		$energy = $energy + int(($date_sec - $last_ene_time)/$sintai_kaihuku);
	}
	$last_ene_time= $date_sec;

	if($energy > $energy_max){$energy = $energy_max;}
	if($energy < 0){$energy = 0;}
	
#==========頭脳パワー計算=============
	if ($in{'iiyudane'} eq "one"){
		$nou_energy = $nou_energy + int(($date_sec - $last_nouene_time)/$zunou_kaihuku*$onsen_times);
	}elsif($in{'iiyudane'} eq "two"){
		$nou_energy = $nou_energy + int(($date_sec - $last_nouene_time)/$zunou_kaihuku*$tokubetu_times);
	}elsif($in{'iiyudane'} eq "five"){
		$nou_energy = $nou_energy + int(($date_sec - $last_nouene_time)/$zunou_kaihuku*$matu_times);
	}elsif($in{'iiyudane'} eq "fo"){
		$nou_energy = $nou_energy + int(($date_sec - $last_nouene_time)/$zunou_kaihuku*$take_times);
	}elsif($in{'iiyudane'} eq "three"){
		$nou_energy = $nou_energy + int(($date_sec - $last_nouene_time)/$zunou_kaihuku*$ume_times);
	}elsif($in{'iiyudane'} eq "six"){
		$nou_energy = $nou_energy + int(($date_sec - $last_nouene_time)/$zunou_kaihuku*$dou_times);
	}elsif($in{'iiyudane'} eq "seven"){
		$nou_energy = $nou_energy + int(($date_sec - $last_nouene_time)/$zunou_kaihuku*$gin_times);
	}elsif($in{'iiyudane'} eq "eight"){
		$nou_energy = $nou_energy + int(($date_sec - $last_nouene_time)/$zunou_kaihuku*$kin_times);
	}else{
		$nou_energy = $nou_energy + int(($date_sec - $last_nouene_time)/$zunou_kaihuku);
	}
	$last_nouene_time= $date_sec;

	if($nou_energy > $nou_energy_max){$nou_energy = $nou_energy_max;}
	if($nou_energy < 0){$nou_energy = 0;}

#==========身体パワーバー（％）算出=============
	if(! $energy_max){$energy_max =1;}
	$ener_parcent = int($energy / $energy_max * 100);
	$ener_parcent_disp = $ener_parcent * 2;
	$nokori_parcent = 200-$ener_parcent_disp;
	if ($ener_parcent >59){$energy_bar = "energy_ao.gif";}
	elsif ($ener_parcent >19){$energy_bar = "energy_ki.gif";}
	else{$energy_bar = "energy_aka.gif";}
	
#==========頭脳パワーバー（％）算出=============
	if(! $nou_energy_max){$nou_energy_max =1;}
	$nou_ener_parcent = int($nou_energy / $nou_energy_max * 100);
	$nou_ener_parcent_ds = $nou_ener_parcent * 2;
	$nou_nokori_parcent = 200-$nou_ener_parcent_ds;
	if ($nou_ener_parcent >59){$nou_energy_bar = "energy_ao.gif";}
	elsif ($nou_ener_parcent >19){$nou_energy_bar = "energy_ki.gif";}
	else{$nou_energy_bar = "energy_aka.gif";}

#==========BMIをチェック=============
	$taijuu = sprintf ("%.1f",$taijuu);
	&check_BMI($sintyou,$taijuu);

#==========コンディション計算=============
		#+++++++++残パワーを加味++++++++++
$condition_sisuu = ($nou_ener_parcent + $ener_parcent) / 2;
		#+++++++++健康値を加味++++++++++
$condition_sisuu += $kenkou / 100;
		#+++++++++空腹度を加味++++++++++
if ($kuuhukudo eq "<font color=#ff3300>満腹（まだ食事できません）</font>"){$condition_sisuu *= 0.8;}elsif ($kuuhukudo eq "丁度いい"){$condition_sisuu *= 1;} elsif ($kuuhukudo eq "やや空腹"){$condition_sisuu *= 0.9;} elsif ($kuuhukudo eq "空腹"){$condition_sisuu *= 0.7;} elsif ($kuuhukudo eq "かなり空腹"){$condition_sisuu *= 0.6;} elsif ($kuuhukudo eq "すごい空腹"){$condition_sisuu *= 0.5;}else{$condition_sisuu *= 0.3;}
		#+++++++++体系指数を加味++++++++++
if ($taikei eq "肥満"){$condition_sisuu *= 0.8;}elsif ($taikei eq "やや太り気味"){$condition_sisuu *= 0.95;} elsif ($taikei eq "標準"){$condition_sisuu *= 1;} elsif ($taikei eq "やせ気味"){$condition_sisuu *= 0.95;} else{$condition_sisuu *= 0.8;} 

if($condition_sisuu > 98) {$condition = "最高"; $byouki_sisuu += 2}
elsif($condition_sisuu > 75) {$condition = "良好"; $byouki_sisuu += 1}
elsif($condition_sisuu > 50) {$condition = "普通";}
elsif($condition_sisuu > 30) {$condition = "不良"; $byouki_sisuu -= -1}
elsif($condition_sisuu > 10) {$condition = "悪い"; $byouki_sisuu -= 3}
else{$condition = "最悪";}

if ($byouki_sisuu < -100){$byoumei = "癌";}
elsif  ($byouki_sisuu < -70){$byoumei = "脳腫瘍";}
elsif  ($byouki_sisuu < -40){$byoumei = "結核";}
elsif  ($byouki_sisuu < -20){$byoumei = "肺炎";}
elsif  ($byouki_sisuu < -15){$byoumei = "下痢";}
elsif  ($byouki_sisuu < -10){$byoumei = "風邪";}
elsif  ($byouki_sisuu < 0){$byoumei = "風邪ぎみ";}
else {$byoumei = "";}

if ($byoumei){$condition = "<font color=#ff6600>$byoumei</font>";}

#==========ジョブレベル算出=============
	$job_level = int($job_keiken / 100) ;

#==========ホスト保存=============
	$host = $get_host;
	
#==========ログイン非表示on off=============
	if ($in{'sanka_hyouzi_on'} eq "off"){$mise_type = "off";}
	if ($in{'sanka_hyouzi_on'} eq "on"){$mise_type = "on";}

#==========最終アクセス保存=============
	$last_access_byou = $access_byou;
	if ($in{'mode'} ne "syokudou" && $in{'mode'} ne "school" && $in{'mode'} ne "gym"){
		$access_byou = $date_sec;
	}

#==========ログインモードならコマンドボタンを表示=============
if ($in{'mode'} eq "login_view"){
	&command_botan;
	
#==========制限時間があれば制限表示=============
		if ($koudou_seigen > 0){
					$ato_nanbyou=$koudou_seigen-($seigenyou_now_time - $last_access_byou);
		}
}

#==========紹介キー=============
	if ($syokai eq 'yes'){
		$no = $k_id;
		if(!$syoukai_id){
			@arufabet = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z');
			$moji1 = $arufabet[int(rand(26))];
			$moji2 = $arufabet[int(rand(26))];
			$suuji = sprintf("%02d",int(rand(100)));
			$moji3 = $arufabet[int(rand(26))];
			$moji4 = $arufabet[int(rand(26))];
			$syoukai_id = "$moji1$moji2$suuji$moji3$moji4";
		}
	}
	
#==========いろいろ=============
$next_levelup = 100 - ($job_keiken % 100);

	if ($dairekutoin eq 'yes2'||$dairekutoin eq 'yes3'){&kingakusyori;} 

	$money1 = $money;
	if ($money1 =~ /^[-+]?\d\d\d\d+/g) {
		  for ($i = pos($money1) - 3, $j = $money1 =~ /^[-+]/; $i > $j; $i -= 3) {
   			 substr($money1, $i, 0) = ',';
  		}
	}
	$k_sousisan1 = $k_sousisan;
		if ($k_sousisan1 =~ /^[-+]?\d\d\d\d+/g) {
  			for ($i = pos($k_sousisan1) - 3, $j = $k_sousisan1 =~ /^[-+]/; $i > $j; $i -= 3) {
    			substr($k_sousisan1, $i, 0) = ',';
  		}
	}

	if (-e $job_keiken_f){
		open (IN,"< $job_keiken_f") || &error("ファイルを開くことが出来ませんでした。");
		eval{ flock (IN, 2); };
		$job_keiken0 = <IN>;
		close(IN);
	}
	chomp $job_keiken0;
	if ($job_keiken0){$disp_job = "<span class=honbun2>履歴書</span>：$job_keiken0";}
	
#==========配偶者、恋人の表示=============
					open(COA,"< $couple_file") || &error("$couple_fileに書き込めません");
					eval{ flock (COA, 2); };
						@all_couple = <COA>;
					close(COA);
					foreach (@all_couple){
						($cn_number,$cn_name1,$cn_name2,$cn_joutai,$cn_total_aijou,$cn_omoide1,$cn_omoide2,$cn_omoide3,$cn_omoide4,$cn_omoide5,$cn_kodomo,$cn_yobi1,$cn_yobi2,$cn_yobi3,$cn_yobi4,$cn_yobi5)= split(/<>/);
						if ($name eq "$cn_name1"){
							if ($cn_joutai eq "恋人"){$my_koibito .= "$cn_name2　";}
							elsif ($cn_joutai eq "配偶者"){$my_haiguusya = "$cn_name2";}
						}
						if ($name eq "$cn_name2"){
							if ($cn_joutai eq "恋人"){$my_koibito .= "$cn_name1　";}
							elsif ($cn_joutai eq "配偶者"){$my_haiguusya = "$cn_name1";}
						}
					}
					
#==========所有物の表示=============
	if(!@my_kounyuu_list){
		$monokiroku_file="./member/$k_id/mono.cgi";
		open(OUT,"< $monokiroku_file") || &error("自分の購入物ファイルが開けません");
		eval{ flock (OUT, 2); };
		@my_kounyuu_list =<OUT>;
		close(OUT);
	}
	foreach (@my_kounyuu_list){
		&syouhin_sprit ($_);
		if($syo_syubetu eq 'ギフト'){
			push @syubetu1,$_;
		}elsif($syo_syubetu eq 'ギフト商品'){
			push @syubetu2,$_;
			if($syo_taikyuu > 0){$morai_itemsuu++;} #koko2007/10/31
		}else{
			push @syubetu3,$_;
			if($syo_taikyuu > 0){$moti_itemsuu++;} #koko2007/10/31
		}
	}
	
	$syouhin_itiran .= "<table border=0 cellpadding=0 cellpadding=0 width=100%><tr><td width=50%><font color=#ff0099>購入商品：$moti_itemsuu個 / $syoyuu_gendosuu個</font><br>";
	
	open (IN,"< $ori_ie_list") || &error("$ori_ie_listファイルを開くことが出来ませんでした。");
	eval{ flock (IN, 1); };
	@orie_list = <IN>;
	close(IN);

	$ie_attayo = 0;
	foreach(@orie_list){
		&ori_ie_sprit($_);
		if($in{'name'} eq $ori_ie_name){
			$ie_attayo =1;
			last;
		}
	}

	$now_time = time; #koko2008/04/08
	foreach (@syubetu3){
		&syouhin_sprit ($_);

		if ($syo_taikyuu_tani eq "日"){#koko2008/04/08
			
			$keikanissuu = int (($now_time - $syo_kounyuubi) / (60*60*24));
			$nokorinissuu = $syo_taikyuu - $keikanissuu;
			if ($nokorinissuu <= 0){next;}
			$syo_taikyuu = $nokorinissuu;
		}#koko2008/04/08end

		if ($syo_taikyuu <=0){next;}
		if ($syo_hinmoku eq "いとしき我が家" && $ie_attayo == 1){ #end2007/11/21
			print <<"EOM";
<table boader=0 width=100%><tr><form method=POST action="original_house.cgi"><td><input type=hidden name=mode value="houmon"><input type=hidden name=name value="$in{'name'}"><input type=hidden name=pass value="$in{'pass'}"><input type=hidden name=k_id value="$k_id"><input type=hidden name=town_no value="$in{'town_no'}"><input type=hidden name=ori_ie_id value="$k_id"><input type=image src='$img_dir/go_home2.gif' width=100 height=10></td></form></tr></table>
EOM
			next;
		}

		#+++++++++持ってる数を出す++++++++++
		if ($kazu_disp eq 'yes'){
			if($syo_siyou_date + ($syo_kankaku*60) > time || (($syo_syubetu eq "食料品" || $syo_syubetu eq "ファーストフード") && time < $last_syokuzi + ($syokuzi_kankaku*60))){
				$syouhin_itiran .= "★$syo_hinmoku($syo_taikyuu$syo_taikyuu_tani)<br>";
			}elsif($syo_syubetu eq "ギフト"){
				$syouhin_itiran .= "◆$syo_hinmoku($syo_taikyuu$syo_taikyuu_tani)<br>";
			}else{
				$syouhin_itiran .= "●$syo_hinmoku($syo_taikyuu$syo_taikyuu_tani)<br>";
			}
		}else{
			if($syo_siyou_date + ($syo_kankaku*60) > time || (($syo_syubetu eq "食料品" || $syo_syubetu eq "ファーストフード") && time < $last_syokuzi + ($syokuzi_kankaku*60))){
				$syouhin_itiran .= "★$syo_hinmoku<br>";
			}elsif($syo_syubetu eq "ギフト"){
				$syouhin_itiran .= "◆$syo_hinmoku<br>";
			}else{
				$syouhin_itiran .= "●$syo_hinmoku<br>";
			}
		}
	}
	$syouhin_itiran .= "</td><td width=50% valign=top><font color=#ff0099>ギフトもらった商品：$morai_itemsuu個 / $gift_gendo個</font><br>";
	foreach (@syubetu2){
		&syouhin_sprit ($_);

		if ($syo_taikyuu <=0){next;}
		if ($syo_hinmoku eq "いとしき我が家"){
			$syouhin_itiran .= <<"EOM";
"<table boader=0 width=100%><tr><form method=POST action=\\"original_house.cgi\\"><td><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>houmon<>\"><input type=hidden name=ori_ie_id value=\\"$k_id\\"><input type=image src='$img_dir/go_home2.gif' width=100 height=10></td></form></tr></table><br>"+
EOM
			next;
		}
		if ($kazu_disp eq 'yes'){
			if($syo_siyou_date + ($syo_kankaku*60) > time || (($syo_syubetu eq "食料品" || $syo_syubetu eq "ファーストフード") && time < $last_syokuzi + ($syokuzi_kankaku*60))){
				$syouhin_itiran .= "★$syo_hinmoku($syo_taikyuu$syo_taikyuu_tani)<br>";
			}elsif($syo_syubetu eq "ギフト"){
				$syouhin_itiran .= "◆$syo_hinmoku($syo_taikyuu$syo_taikyuu_tani)<br>";
			}else{
				$syouhin_itiran .= "●$syo_hinmoku($syo_taikyuu$syo_taikyuu_tani)<br>";
			}
		}else{
			if($syo_siyou_date + ($syo_kankaku*60) > time || (($syo_syubetu eq "食料品" || $syo_syubetu eq "ファーストフード") && time < $last_syokuzi + ($syokuzi_kankaku*60))){
				$syouhin_itiran .= "★$syo_hinmoku<br>";
			}elsif($syo_syubetu eq "ギフト"){
				$syouhin_itiran .= "◆$syo_hinmoku<br>";
			}else{
				$syouhin_itiran .= "●$syo_hinmoku<br>";
			}
		}
	}
	$mochikazu = $#syubetu1 + 1;
	$syouhin_itiran .= "<br><font color=#ff0099>ギフト送る商品：$mochikazu個 / $kounyu_gift_gendo個</font><br>";
	foreach (@syubetu1){
		&syouhin_sprit ($_);

		if ($syo_taikyuu <=0){next;}
		if ($kazu_disp eq 'yes'){
			if($syo_siyou_date + ($syo_kankaku*60) > time || (($syo_syubetu eq "食料品" || $syo_syubetu eq "ファーストフード") && time < $last_syokuzi + ($syokuzi_kankaku*60))){
				$syouhin_itiran .= "★$syo_hinmoku($syo_taikyuu$syo_taikyuu_tani)<br>";
			}elsif($syo_syubetu eq "ギフト"){
				$syouhin_itiran .= "◆$syo_hinmoku($syo_taikyuu$syo_taikyuu_tani)<br>";
			}else{
				$syouhin_itiran .= "●$syo_hinmoku($syo_taikyuu$syo_taikyuu_tani)<br>";
			}
		}else{
			if($syo_siyou_date + ($syo_kankaku*60) > time || (($syo_syubetu eq "食料品" || $syo_syubetu eq "ファーストフード") && time < $last_syokuzi + ($syokuzi_kankaku*60))){
				$syouhin_itiran .= "★$syo_hinmoku<br>";
			}elsif($syo_syubetu eq "ギフト"){
				$syouhin_itiran .= "◆$syo_hinmoku<br>";
			}else{
				$syouhin_itiran .= "●$syo_hinmoku<br>";
			}
		}
	}
	
	$syouhin_itiran .= "</td></tr></table>";
#==========能力バーの表示=============
	$nouryoku_goukeiti = $kokugo + $suugaku + $rika + $syakai + $eigo + $ongaku + $bijutu + $looks + $tairyoku + $kenkou + $speed + $power + $wanryoku + $kyakuryoku;
	if($nouryoku_goukeiti){
		foreach (6..22){
			$nouryoku_bar[$_] = int (($nouryoku_suuzi_hairetu[$_] / $nouryoku_goukeiti)*5000);
		}
	}

#==========オークションや株===========#
	if (-e "$auction_log"){
		open(IN,"< $auction_log") || &error("Open Error : $auction_log");
		eval{ flock (IN, 1); };
		@auction_dat = <IN>;
		close(IN);
		
		$i=0;
		foreach (@auction_dat){
			if($i >= 5){
				last;
				$auc1 .= "etc..."
			}
			($auc_dat,$syo_dat) = split(/\t\t/);
			($auc_name,$auc_id,$auc_t_name,$auc_t_id,$auc_soku,$auc_strat,$auk_haba,$auc_ima,$auc_e_tim,$auc_end_t,$auc_rak_tim,$auc_rak_kakaku,$auc_end,$euc_s_subetu,$euc_s_syohin,$com_syupin,$com_sanka) = split(/<>/,$auc_dat);
			if(!$auc_end){
				$auc1 .= "<font color=#ffffff>$auc_nameさんの<b>$euc_s_syohin</b>（現在：$auc_ima円）　　</font>";
			}
			$i++;
		}
	}
	if(!$auc1){$auc1 .="<font color=#ffffff>現在出品中の商品はありまへん。</font>";}
	
	open(IN,"./log_dir/kab_hendou.cgi") || &error("Open Error : ./log_dir/kab_hendou.cgi");
	eval{ flock (IN, 2); };
	$kab_dat = <IN>;
	close(IN);
	($kabukaA,$kabukaB,$kabukaC,$kabukaD,$kabukaE) = split(/<>/,$kab_dat);

#==========ステータスなどの表示=============
	if (int(rand(3))+1 == 1){
		$aisatu_style = "style=\"position:absolute;display:none;\"";
		$aisatu_style2 = "style=\"position:absolute;display:none;\"";
	}elsif(int(rand(3))+1 == 2){
		$enq_style = "style=\"position:absolute;display:none;\"";
		$aisatu_style2 = "style=\"position:absolute;display:none;\"";
	}else{
		$enq_style = "style=\"position:absolute;display:none;\"";
		$aisatu_style = "style=\"position:absolute;display:none;\"";
	}
	
	#==========ログ更新=============
	&temp_routin;
	&log_kousin($my_log_file,$k_temp);
	
	print <<"EOM";
<style type="text/css"><!--
	#menu{
		cursor:pointer;
		font-weight: bold;
		border: 3px #339966 solid;
		border-width: 3px 3px 0px 3px;
		background-color: #C8C8C8;
		width: 30%;
	}
	#menu2{
		cursor:pointer;
		font-weight: bold;
		border: 3px #339966 solid;
		border-width: 0px 3px 3px 3px;
		background-color: #C8C8C8;
		width: 30%;
	}
 --></style>
<Script Language="JavaScript"><!--
	var TimeID;
	var counts=$koudou_seigen;
	window.setTimeout("run()",1000);
	function run(){
		counts--;
		document.getElementById("timeleft").innerHTML = counts;
		if(counts>0){timeID = setTimeout("run()",1000);}
	}
	
	function Change(place){
		place.style.backgroundColor="#339966";
		place.style.color='#ffffff';
	}
	function Back(place){
		place.style.backgroundColor='';
		place.style.color='';
	}
	
	function menu(ima,tugi){
		if(document.all){
			document.all(ima).style.position = "absolute";
			document.all(ima).style.display = "none";
			document.all(tugi).style.position = "static";
			document.all(tugi).style.display = "block";
		}else if(document.getElementById){
			document.getElementById(ima).style.position = "absolute";
			document.getElementById(ima).style.display = "none";
			document.getElementById(tugi).style.position = "static";
			document.getElementById(tugi).style.display = "block";
		}
	}
//--></script>

<table width="100%" border="0"  cellspacing="0" cellpadding="2" style=" border: $st_win_wak; border-style: solid; border-width: 2px;" bgcolor=$st_win_back><tr>$top_botan</tr></table>
<br>
<table bgcolor="#000000" width="100%" border="0"  cellspacing="0" cellpadding="2" style=" border: $st_win_wak; border-style: solid; border-width: 2px;"><tr><td>

	<table width="100%">
	<tr>
	<td align="left">
		<span style="color:#ffffff;font-size:11px;">行動できるまであと<span id="timeleft">$koudou_seigen</span>秒</span>
	</td>
	<td align="right">
		<span id="j_time" style="color:#ffffff;font-size:11px;"></span>
	</td>
	</tr>
	</table>
	<marquee scrollamount="5">
    <font color=#ff0000>株情報</font>　　<font color=#ffffff>大阪株：$kabukaA円　滋賀株：$kabukaB円　兵庫株：$kabukaC円　奈良株：$kabukaD円　近畿株：$kabukaE円</font>　　　　　<font color=#ff0000>オークション情報</font>　　<font color=#ffffff>$auc1</font>
    </marquee>
    
</td></tr></table>
<br>

<div id="enq" $enq_style>
<table width="100%" cellspacing="0" cellpadding="5"><tr align="center">
<td onclick="menu('enq','stetas')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu">ステータス</td>
<td> </td>
<td onclick="menu('enq','item')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu">アイテム</td>
<td> </td>
<td onclick="menu('enq','nouryoku')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu">能\力値</td>
</tr></table>
<table border="2" bordercolor="#339966" cellspacing="0" cellpadding="2" bgcolor="#ffffff" width=100%><tr><td>
$enq_table
</td></tr></table>
<table width="100%" cellspacing="0" cellpadding="5"><tr align="center">
<td bgcolor="#339966" width="30%"><font color="#ffffff"><b>アンケート</b></font></td>
<td> </td>
<td onclick="menu('enq','senden')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu2">宣伝</td>
<td> </td>
<td onclick="menu('enq','kanrinin')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu2">管理人</td>
</tr></table>
</div>

<div id="senden" $aisatu_style>
<table width="100%" cellspacing="0" cellpadding="5"><tr align="center">
<td onclick="menu('senden','stetas')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu">ステータス</td>
<td> </td>
<td onclick="menu('senden','item')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu">アイテム</td>
<td> </td>
<td onclick="menu('senden','nouryoku')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu">能\力値</td>
</tr></table>
<table border="2" bordercolor="#339966" cellspacing="0" cellpadding="2" bgcolor="#ffffff" width=100%><tr><td>
<center>宣伝</center>
$aisatu_table3
</td></tr></table>
<table width="100%" cellspacing="0" cellpadding="5"><tr align="center">
<td onclick="menu('senden','enq')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu2">アンケート</td>
<td> </td>
<td bgcolor="#339966" width="30%"><font color='#ffffff'><b>宣伝</b></font></td>
<td> </td>
<td onclick="menu('senden','kanrinin')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu2">管理人より</td>
</tr></table>
</div>

<div id="kanrinin" $aisatu_style2>
<table width="100%" cellspacing="0" cellpadding="5"><tr align="center">
<td onclick="menu('kanrinin','stetas')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu">ステータス</td>
<td> </td>
<td onclick="menu('kanrinin','item')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu">アイテム</td>
<td> </td>
<td onclick="menu('kanrinin','nouryoku')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu">能\力値</td>
</tr></table>
<table border="2" bordercolor="#339966" cellspacing="0" cellpadding="2" bgcolor="#ffffff" width=100%><tr><td>
<center>管理人からのメッセージ</center>
$aisatu_table2
</td></tr></table>
<table width="100%" cellspacing="0" cellpadding="5"><tr align="center">
<td onclick="menu('kanrinin','enq')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu2">アンケート</td>
<td> </td>
<td onclick="menu('kanrinin','senden')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu2">宣伝</td>
<td> </td>
<td bgcolor="#339966" width="30%"><font color="#ffffff"><b>管理人より</td>
</tr></table>
</div>

<div id="stetas" style="position:absolute;display:none;">
<table width="100%" cellspacing="0" cellpadding="5"><tr align="center">
<td bgcolor="#339966" width="30%"><font color="#ffffff"><b>ステータス</b></font></td>
<td> </td>
<td onclick="menu('stetas','item')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu">アイテム</td>
<td> </td>
<td onclick="menu('stetas','nouryoku')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu">能\力値</td>
</tr></table>
<table border="2" bordercolor="#339966" cellspacing="0" cellpadding="2" bgcolor="#ffffff" width=100%><tr><td>
<span class=honbun2 onMouseOver="Navi('$img_dir/about.gif', 'ＩＤとは', 'ＩＤは登録番号です。<br>つまり何番目に登録したかということです。', 1, event);" onMouseOut="NaviClose();">名　前（ID)</span>：$name（$k_id）<br>
<span class=honbun2>パスワード</span>：$pass<br>
<span class=honbun2 onMouseOver="Navi('$img_dir/about.gif', '紹介コードとは', '紹介コードを教えて紹介すると、お金がもらえます。<br>登録時に紹介コードを入力してもらう必要があります。', 1, event);" onMouseOut="NaviClose();">紹介コード：</span>$syoukai_id=$no<br>
<span class=honbun2>ブラウザ</span>:$brauza<br>
<span class=honbun2>持ち金</span>：$money1円<span class=small onMouseOver="Navi('$img_dir/about.gif', '総資産とは', '総資産＝持ち金 + 普通預金 + スーパー定期 - ローン額', 1, event);" onMouseOut="NaviClose();">（総資産：$k_sousisan1円）</span><br>
<span class=honbun2 onMouseOver="Navi('$img_dir/about.gif', '経験値', '経験地は$job_keikenです。<br>次のレベルアップまであと$next_levelup<br>勤務数：$job_kaisuu回', 1, event);" onMouseOut="NaviClose();">職　業</span>：$job（レベル $job_level）<br>
<span class=honbun2 onMouseOver="Navi('$img_dir/about.gif', 'Ｋポイント', 'ＫＩＮＫＩポイントの略で、単位はＰです。<br>アイデアが採用されたり、街を活発にすることなどであがります。<br>この数値が大きいほどなにか特権がもらえます。', 1, event);" onMouseOut="NaviClose();">Ｋポイント</span>：$kpointＰ<br>
$disp_job
<span class=honbun2 onMouseOver="Navi('$img_dir/about.gif', '身体パワーとは', '$sintai_kaihuku秒に１ポイント回復します。<br>MAX値は身体パラメータを上げることで増加します。', 1, event);" onMouseOut="NaviClose();">身体パワー</span>：$energy （MAX値：$energy_max）<br><img src="$img_dir/$energy_bar" width="$ener_parcent_disp" height="8"><img src="$img_dir/nokori_bar.gif" width="$nokori_parcent" height="8"><br>
<span class=honbun2 onMouseOver="Navi('$img_dir/about.gif', '頭脳パワーとは', '$zunou_kaihuku秒に１ポイント回復します。<br>MAX値は頭脳パラメータを上げることで増加します。', 1, event);" onMouseOut="NaviClose();">頭脳パワー</span>：$nou_energy（MAX値：$nou_energy_max）<br><img src="$img_dir/$nou_energy_bar" width="$nou_ener_parcent_ds" height="8"><img src="$img_dir/nokori_bar.gif" width="$nou_nokori_parcent" height="8"> <br>
<span class=honbun2 onMouseOver="Navi('$img_dir/about.gif', 'コンディションとは', 'コンディションは「パワー」の回復度に最も影響を受けます。<br>他にも仕事などに関係します。', 1, event);" onMouseOut="NaviClose();">コンディション</span>：$condition<br>
<span class=honbun2>身　　長</span>：$sintyou cm<br>
<span class=honbun2>体　　重</span>：$taijuu kg<br>
<span class=honbun2 onMouseOver="Navi('$img_dir/about.gif', '体格指数とは', '体格指数(BMI) = 体重(kg) ÷ 身長(m) ÷ 身長(m)', 1, event);" onMouseOut="NaviClose();">体格指数</span>：$BMI（$taikei）<br>
<span class=honbun2 onMouseOver="Navi('$img_dir/about.gif', '空腹度とは', '満腹でなければ食事をすることができます。<br>前回の食事は$last_syokuzi_henkanです。', 1, event);" onMouseOut="NaviClose();">空腹度</span>：$kuuhukudo<br>
<span class=honbun2>配偶者</span>：$my_haiguusya<br>
<span class=honbun2>恋　人</span>：$my_koibito<br>
</td></tr></table>
<table width="100%" cellspacing="0" cellpadding="5"><tr align="center">
<td onclick="menu('stetas','enq')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu2">アンケート</td>
<td> </td>
<td onclick="menu('stetas','senden')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu2">宣伝</td>
<td> </td>
<td onclick="menu('stetas','kanrinin')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu2">管理人より</td>
</tr></table>
</div>

<div id="item" style="position:absolute;display:none;">
<table width="100%" cellspacing="0" cellpadding="5"><tr align="center">
<td onclick="menu('item','stetas')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu">ステータス</td>
<td> </td>
<td bgcolor="#339966" width="30%"><font color="#ffffff"><b>アイテム</b></font></td>
<td> </td>
<td onclick="menu('item','nouryoku')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu">能\力値</td>
</tr></table>
<table border="2" bordercolor="#339966" cellspacing="0" cellpadding="2" bgcolor="#ffffff" width=100%><tr><td>
$syouhin_itiran
</td></tr></table>
<table width="100%" cellspacing="0" cellpadding="5"><tr align="center">
<td onclick="menu('item','enq')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu2">アンケート</td>
<td> </td>
<td onclick="menu('item','senden')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu2">宣伝</td>
<td> </td>
<td onclick="menu('item','kanrinin')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu2">管理人より</td>
</tr></table>
</div>

<div id="nouryoku" style="position:absolute;display:none;">
<table width="100%" cellspacing="0" cellpadding="5"><tr align="center">
<td onclick="menu('nouryoku','stetas')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu">ステータス</td>
<td> </td>
<td onclick="menu('nouryoku','item')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu">アイテム</td>
<td> </td>
<td bgcolor="#339966" width="30%"><font color="#ffffff"><b>能\力値</b></font></td>
</tr></table>
<table border="2" bordercolor="#339966" cellspacing="0" cellpadding="2" style="font-size:10px;line-height:10px;" bgcolor=$st_win_back width=100%><tr><td width=50%>
<table><td align=center><span class=tyuu>頭　脳</span></td></tr>
<tr><td><table class=small><tr><td width=$nouryoku_bar[6] bgcolor=#ffcc00>国語：$kokugo</td></tr></table></td></tr>
<tr><td><table class=small><tr><td width=$nouryoku_bar[7] bgcolor=#ffcc00>数学：$suugaku</td></tr></table></td></tr>
<tr><td><table class=small><tr><td width=$nouryoku_bar[8] bgcolor=#ffcc00>理科：$rika</td></tr></table></td></tr>
<tr><td><table class=small><tr><td width=$nouryoku_bar[9] bgcolor=#ffcc00>社会：$syakai</td></tr></table></td></tr>
<tr><td><table class=small><tr><td width=$nouryoku_bar[10] bgcolor=#ffcc00>英語：$eigo</td></tr></table></td></tr>
<tr><td><table class=small><tr><td width=$nouryoku_bar[11] bgcolor=#ffcc00>音楽：$ongaku</td></tr></table></td></tr>
<tr><td><table class=small><tr><td width=$nouryoku_bar[12] bgcolor=#ffcc00>美術：$bijutu</td></tr></table></td></tr></table>
</td></tr><tr><td>
<table><tr><td align=center><span class=tyuu>身　体</span></td></tr>
<tr><td><table class=small><tr><td width=$nouryoku_bar[13] bgcolor=#ffcc00>ルックス：$looks</td></tr></table></td></tr>
<tr><td><table class=small><tr><td width=$nouryoku_bar[14] bgcolor=#ffcc00>体力：$tairyoku</td></tr></table></td></tr>
<tr><td><table class=small><tr><td width=$nouryoku_bar[15] bgcolor=#ffcc00>健康：$kenkou</td></tr></table></td></tr>
<tr><td><table class=small><tr><td width=$nouryoku_bar[16] bgcolor=#ffcc00>スピード：$speed</td></tr></table></td></tr>
<tr><td><table class=small><tr><td width=$nouryoku_bar[17] bgcolor=#ffcc00>パワー：$power</td></tr></table></td></tr>
<tr><td><table class=small><tr><td width=$nouryoku_bar[18] bgcolor=#ffcc00>腕力：$wanryoku</td></tr></table></td></tr>
<tr><td><table class=small><tr><td width=$nouryoku_bar[19] bgcolor=#ffcc00>脚力：$kyakuryoku</td></tr></table></td></tr></table>
</td></tr><tr><td>
<table><tr><td align=center><span class=tyuu>その他</span></td>
<tr><td><table class=small><tr><td width=$nouryoku_bar[20] bgcolor=#ffcc00>LOVE：$love</td></tr></table></td></tr>
<tr><td><table class=small><tr><td width=$nouryoku_bar[21] bgcolor=#ffcc00>面白さ：$unique</td></tr></table></td></tr>
<tr><td><table class=small><tr><td width=$nouryoku_bar[22] bgcolor=#ffcc00>エッチ：$etti</td></tr></table></td></tr>
</table>
</td></tr></table>
<table width="100%" cellspacing="0" cellpadding="5"><tr align="center">
<td onclick="menu('nouryoku','enq')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu2">アンケート</td>
<td> </td>
<td onclick="menu('nouryoku','senden')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu2">宣伝</td>
<td> </td>
<td onclick="menu('nouryoku','kanrinin')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu2">管理人より</td>
</tr></table>
</div>
EOM
		if($hozontown eq 'yes'){$disp_tag = "<input type=\"hidden\" name=\"town_no\" value=\"$ck{'town_no'}\">\n";}else{$disp_tag="";}
		
		
#---------------金額処理（内部）-------------------#
sub kingakusyori{
	if(!$in{'fragu'}){
		$in{'mae_town'} = $in{'town_no'};
		$in{'fragu'} = 1;
	}elsif($in{'mae_town'} != $in{'town_no'}){
		$money =~ s/\,//g;
		$money -= 100000;
		&temp_routin;
		&log_kousin($my_log_file,$k_temp);

		$in{'mae_town'} = $in{'town_no'};

	}
}


}

#---------------ログバックアップ処理-------------------#
sub list_log_backup {
					use DirHandle;
					$dir = new DirHandle ("./log_dir");
					while($file_name = $dir->read){
							if($file_name eq '.' || $file_name eq '..' || $file_name =~ /^backup_/ || $file_name eq '.DS_Store'){next;}
							my $backup_name = "backup_" ."$file_name";
							open (BK,"< ./log_dir/$file_name")  || &error("Open Error : ./log_dir/$file_name");
							eval{ flock (BK, 2); };
							my @back_data = <BK>;
							close (BK);
							if (@back_data != ""){
								open (BKO,">./log_dir/backup_dir/$backup_name") || &error("Write Error : ./log_dir/backup_dir/$backup_name");
								eval{ flock (BKO, 2); };
								print BKO @back_data;
								close (BKO);
							}
					}
					$dir->close;
}