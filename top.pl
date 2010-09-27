#######################################
#　隠し名前を表示させるか　'#ffffff' 色指定表示　'' 表示無し
$name_disp = '#ff0000';
#　参加者のバックカラー　'style="background: #ffffff"' 背景色指定 '' 表示無し
$neme_back = 'size=2 style="background: "';
# タイムスタンプを表示　'yes'の時
$time_stanpu = 'yes';
# 管理者の名前(この名前の管理者だけ表示)
@kanri_name = ();
#新しい更新情報
$reload = <<"EOM";
EOM
# 文字色の指定　0 番目の街から順番に
@mojisyoku = ('#ff0000','#000000','#0000ff','#ffffff');
#重要なアンケートの内容（ないときは空）
$enq_jyuuyou="";
####################################################
#/////////////////以下サブルーチン/////////////////#
####################################################

sub main_view {
	if ($in{'command'} eq "mati_idou" || $in{'command'} eq "mati_idou2"){
		&header(syokudou_style);
		if ($matiidou_time2 <= 0){
	        $move_com = "<div align=center style=\"font-size:11px\">$idousyudan移動中...<br>すぐにつきます。<br>$disp</div>";
		}else{
			$move_com = "<div align=center style=\"font-size:11px\">$idousyudan移動中...<br><span id=\"time\">$matiidou_time2</span>秒ほどお待ちください。<br>$disp</div>";
		}
		print <<"EOM";
		<script language="JavaScript"><!--
			var TimeID;
			var counts=$matiidou_time2;
			window.setTimeout("run()",1000);
			function run(){
				counts--;
				document.getElementById("time").innerHTML = counts;
				if(counts>0){timeID = setTimeout("run()",1000);}
			}
		//--></script>

		<br><br><br><br><table  border=0  cellspacing="5" cellpadding="0" width=200 align=center bgcolor=#ffffcc><tr><td>
		$move_com
		</td></tr></table>

		<form method=POST name=f_idou action="$script">
		<input type=hidden name=mode value="login_view">
		<input type=hidden name=town_no value="$in{'town_no'}">
		<input type=hidden name=idou value="$idou_time">
		<input type=hidden name=name value="$in{'name'}">
		<input type=hidden name=pass value="$in{'pass'}">
		<input type=hidden name=ziko_flag value="$ziko_flag">
		<input type=hidden name=ziko_idousyudan value="$ziko_idousyudan">
		<input type=hidden name=maigo value="$maigo">
		</form>
EOM
		exit;
	}
	
	#パーツ情報を取得
	&town_no_get;
	&get_unit;
	&kozin_house;
	&simaitosi;
	&simaitosi2;
	&admin_parts;
	
	#####街のログを開いて画面展開
	$town_data = "./log_dir/townlog".$this_town_no.".cgi";
	open(TW,"$town_data") || &error("Open Error : $town_data");
	eval{ flock (TW, 2); }; 
	$hyouzi_town_hairetu = <TW>;
	close(TW);
	
	&town_sprit($hyouzi_town_hairetu);
	#家建築確認画面なら予定地を表示
	if ($in{'mode'} eq "kentiku_do" && $in{'command'} eq "kakunin"){
		$sentaku_point = $in{'tateziku'} + $in{'yokoziku'} ;
		if (!($town_sprit_matrix[$sentaku_point] eq "空地" || $town_sprit_matrix[$sentaku_point] eq "空地2" || $town_sprit_matrix[$sentaku_point] eq "空地3" || $town_sprit_matrix[$sentaku_point] eq "空地4")){
			($ori_k_id0,$temp) = split(/=/, $town_sprit_matrix[$sentaku_point]);
			($ori_k_id_0,$ori_k_no) = split(/_/, $ori_k_id0);
			if ($k_id ne "$ori_k_id_0" && $ori_k_no > 0){
				&error("選択した場所は空き地ではありません！");
			}
		}
		$town_sprit_matrix[$sentaku_point] = "地";
	}
	&header("","sonomati");
	&get_cookie;
	&time_get;
	#街の中の背景色
	if($in{'town_no'} == 0){
		$takasi_bak ='./img/keihansin.gif';
		if($return_hour >= 22){
			$sotonoiro="#333366";
		}elsif ($return_hour >= 18){
			$sotonoiro="#666699";
		}elsif ($return_hour >= 16){
			$sotonoiro="#ff9966";
		}elsif ($return_hour >= 10){
			$sotonoiro="#ffff99";
		}elsif ($return_hour >= 7){
			$sotonoiro="#ffcc66";
		}elsif ($return_hour >= 0){
			$sotonoiro="#333366";
		}
	}elsif ($in{'town_no'} ==1){
		$takasi_bak ='./img/biwako.gif';
		if($return_hour >= 22){
			$sotonoiro="#333366";
		}elsif ($return_hour >= 18){
			$sotonoiro="#666699";
		}elsif ($return_hour >= 16){
			$sotonoiro="#ff9966";
		}elsif ($return_hour >= 10){
			$sotonoiro="#ffff99";
		}elsif ($return_hour >= 7){
			$sotonoiro="#ffcc66";
		}elsif ($return_hour >= 0){
			$sotonoiro="#333366";
		}
	}elsif($in{'town_no'} ==2){
		$takasi_bak ='./img/nara.gif';
		if($return_hour >= 22){
			$sotonoiro="#333366";
		}elsif ($return_hour >= 18){
			$sotonoiro="#666699";
		}elsif ($return_hour >= 16){
			$sotonoiro="#ff9966";
		}elsif ($return_hour >= 10){
			$sotonoiro="#ffff99";
		}elsif ($return_hour >= 7){
			$sotonoiro="#ffcc66";
		}elsif ($return_hour >= 0){
			$sotonoiro="#333366";
		}
	}elsif($in{'town_no'} ==3){
	    $takasi_bak ='./img/wakayama.gif';
		if($return_hour >= 22){
			$sotonoiro="#333366";
		}elsif ($return_hour >= 18){
			$sotonoiro="#666699";
		}elsif ($return_hour >= 16){
			$sotonoiro="#ff9966";
		}elsif ($return_hour >= 10){
			$sotonoiro="#ffff99";
		}elsif ($return_hour >= 7){
			$sotonoiro="#ffcc66";
		}elsif ($return_hour >= 0){
			$sotonoiro="#333366";
		}
	}else{
		$takasi_bak ='./img/land.gif';
		if($return_hour >= 22){
			$sotonoiro="#333366";
		}elsif ($return_hour >= 18){
			$sotonoiro="#666699";
		}elsif ($return_hour >= 16){
			$sotonoiro="#ff9966";
		}elsif ($return_hour >= 10){
			$sotonoiro="#ffff99";
		}elsif ($return_hour >= 7){
			$sotonoiro="#ffcc66";
		}elsif ($return_hour >= 0){
			$sotonoiro="#333366";
		}
	}

	if($in{'mode'} eq "login_view"){
		#メール
		$message_file="./member/$k_id/mail.cgi";
		open(MS,"< $message_file") || &error("自分のメールログファイルが開けません");
		eval{ flock (MS, 2); };
		$lastCheckTime=<MS>;#最終メール時間の取得
		@lastMailTime=<MS>;#メールデータ配列
		close(MS);
		foreach (@lastMailTime){
			&mail_sprit($_);
			if ($m_syubetu ne "送信"){$saigono_kita_mail = $m_byou;last;}
		}
    
		$i = 0;
		foreach (@lastMailTime){
			&mail_sprit($_);
			if ($m_syubetu eq "送信"){next;}
			if($lastCheckTime < $m_byou){++$i;}
		}
		@lastMailTime=split(/<>/,$lastMailTime);
		if($i){$i = "$i通の";}else{$i = "";}
		if($lastCheckTime < $saigono_kita_mail){
			$happend_houkoku .= "<div style=color:#ff3300>★受信箱に$i新しいメッセージが届いています！</div>";
		}

		#掲示板
		$bbs1_log_file = "./member/$k_id/bbs1_log.cgi";
		if (-e "$bbs1_log_file"){
			open(IN,"< $bbs1_log_file") || &error("Open Error : $bbs1_log_file");
			eval{ flock (IN, 2); };
			$total_counter = <IN>;
			close(IN);
			($total_counter,$all_total_counter,$kakikomijikan,$yomidashijikan)= split(/<>/, $total_counter);
			if ($yomidashijikan < $kakikomijikan){
				$happend_houkoku .= "<div style=color:#ff3300>★掲示板に新規書込があります！</div>";
			}
		}
    
		#会社掲示板
		if (-e "./member/$k_id/kaishiya_bbs.cgi"){
			open(KAISYA,"< ./member/$k_id/kaishiya_bbs.cgi") || &error("kaishiya_bbs.cgiファイルを開くことが出来ませんでした。");
			eval{ flock (KAISYA, 2); };
			$kanri_bbs = <KAISYA>;
			@kiji_bbs = <KAISYA>;
			close(KAISYA);

			($opn_no,$men_no,$kai_id,$kai_name_kanre,$kaitime,$kakikomijikan,$yomidashijikan) = split(/<>/,$kanri_bbs);
			if ($yomidashijikan < $kakikomijikan){
				$happend_houkoku .= "<div style=color:#ff3300>★会社掲示板に新規書込があります！</div>";
			}
		}
	
		#アンケート
		if($enq_jyuuyou){
			open(ENQ,"< ./member/1/enq_member.cgi") || &error("./member/1/enq_member.cgiを開くことが出来ませんでした。");
			eval{ flock (ENQ, 2); };
			@member = <ENQ>;
			foreach(@member){
				chomp $_;
				if($name eq $_){$enq_toukouzumi="1";}
			}
			close(ENQ);
			if(!$enq_toukouzumi){
				$happend_houkoku .= $enq_jyuuyou;
			}
		}
		#ゴキブリ
		if($goki eq "on"){
			$goki_speed = int(rand(10))+10;
			$now_goki = time;
			print <<"EOM";
			<script type="text/JavaScript"><!-- 
				setTimeout('goki()', 20000);
				function goki(){
					document.getElementById("goki").style.display = "none";
				}
			  --></script>
			<table width="100%" STYLE="position:absolute;right:50;top:10;z-index:20" id="goki"><tr>
			<form method=POST action="town_maker.cgi"><td>
			<input type=hidden name=goki_time value="$now_goki">
			<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>login_view<>">
			<input type=hidden name=goki value="on">
			<MARQUEE scrollamount="$goki_speed" behavior="alternate">
			<input type=image src='img/goki.gif'>
			</MARQUEE>
			</td></form>
			</tr></table>
EOM
		}
#==========最後に食事した時間を日付に変換=============
		&byou_hiduke($last_syokuzi);
		$last_syokuzi_henkan = $bh_full_date;
		#+++++++++空腹度を算出++++++++++
		$tabetenaizikan = $date_sec - $last_syokuzi ;
		$manpuku_time = $syokuzi_kankaku*60;
		if ($tabetenaizikan < $manpuku_time){$kuuhukudo = "<font color=#ff3300>満腹（まだ食事できません）</font>";}
		elsif ($tabetenaizikan < $manpuku_time + 60*60*2 ){$kuuhukudo = "丁度いい";}
		elsif ($tabetenaizikan < $manpuku_time + 60*60*12 ){$kuuhukudo = "やや空腹";}
		elsif ($tabetenaizikan < $manpuku_time + 60*60*24 ){$kuuhukudo = "空腹";}
		elsif ($tabetenaizikan < $manpuku_time + 60*60*48 ){$kuuhukudo = "かなり空腹";}
		elsif ($tabetenaizikan < $manpuku_time + 60*60*24*4){$kuuhukudo = "すごい空腹";}
		elsif ($tabetenaizikan < $manpuku_time + 60*60*24*($deleteUser - 5)){$kuuhukudo = "死にそう。。";}
		else{
			$kuuhukudo = "危険！死ぬ寸前です。";
			$happend_houkoku .= "<div style=color:#ff3300><b>このままだと空腹で死んでしまいます！<br>いますぐ食事を取ってデータセーブしましょう！</b><br>（食事をしてもセーブしないといけません。）</div>";
        }
		
		#イベント
		if($happend_ivent){
			$ivent .= <<"EOM";
			<table cellpadding="3" cellspacing="0" style="border: solid 3px #8080C0;" id="table1">
				<tr bgcolor="#8080C0">
					<td align="left"><span style="color:#ffffff;font-size:12px;">イベント発生！</span></td>
					<td align="right" id="title1"><span onclick="event_close('1')" style="cursor:pointer;color:#ffffff;font-size:11px;">×閉じる</span></td>
				</tr>
				<tr bgcolor="#ffffff">
					<td colspan="2" id="box1">$happend_ivent</td>
				</tr>
			</table>
			<br>
EOM
		}
    	
		#報告
		if($happend_houkoku){
			$ivent .= <<"EOM";
			<table cellpadding="3" cellspacing="0" style="border: solid 3px #8080C0;" id="table2">
				<tr bgcolor="#8080C0">
					<td align="left"><span style="color:#ffffff;font-size:12px;">報告があります！</span></td>
					<td align="right" id="title2"><span onclick="event_close('2')" style="cursor:pointer;color:#ffffff;font-size:11px;">×閉じる</span></td>
				</tr>
				<tr bgcolor="#ffffff">
					<td colspan="2" id="box2">$happend_houkoku</td>
				</tr>
			</table>
			<br>
EOM
		}
    
		#あいさつ
		if($happend_aisatu){
			$ivent .= <<"EOM";
			<table cellpadding="3" cellspacing="0" style="border: solid 3px #8080C0;" id="table3">
				<tr bgcolor="#8080C0">
					<td align="left"><span style="color:#ffffff;font-size:12px;">あいさつしました。</span></td>
					<td align="right" id="title3"><span onclick="event_close('3')" style="cursor:pointer;color:#ffffff;font-size:11px;">×閉じる</span></td>
				</tr>
				<tr bgcolor="#ffffff">
					<td colspan="2" id="box3">$happend_aisatu</td>
				</tr>
			</table>
EOM
		}
    
		#表示
		if($ivent){
			print <<"EOM";
			<script type="text/JavaScript"><!-- 
				function event_close(suuji){
					document.getElementById("table" + suuji).width = "200";
					document.getElementById("box" + suuji).style.display = "none";
					document.getElementById("title" + suuji).innerHTML = "<span onclick='event_open(" + suuji + ")' style='cursor:pointer;color:#ffffff;font-size:11px;'>○開く</span>";
				}
				function event_open(suuji){
					document.getElementById("table" + suuji).width = "";
					document.getElementById("box" + suuji).style.display = "block";
					document.getElementById("title" + suuji).innerHTML = "<span onclick='event_close(" + suuji + ")' style='cursor:pointer;color:#ffffff;font-size:11px;'>×閉じる</span>";
				}
			  --></script>
			<table style="position:absolute;top:0;z-index:1;right:10;"><tr><td align="right">
			$ivent
			</td></tr></table>
EOM
		}

	}else{
		print <<"EOM";
		<script type="text/JavaScript"><!-- 
			function event_close(suuji){
				document.getElementById("table" + suuji).width = "200";
				document.getElementById("box" + suuji).style.display = "none";
				document.getElementById("title" + suuji).innerHTML = "<span onclick='event_open(" + suuji + ")' style='cursor:pointer;color:#ffffff;font-size:11px;'>○開く</span>";
			}
			function event_open(suuji){
				document.getElementById("table" + suuji).width = "";
				document.getElementById("box" + suuji).style.display = "block";
				document.getElementById("title" + suuji).innerHTML = "<span onclick='event_close(" + suuji + ")' style='cursor:pointer;color:#ffffff;font-size:11px;'>×閉じる</span>";
			}
		  --></script>
		<table cellpadding="5" cellspacing="0" style="position:absolute;top:0;z-index:1;right:10;border: solid 3px #8080C0;" id="table1">
			<tr bgcolor="#8080C0">
				<td align="left"><span style="color:#ffffff;font-size:12px;">更新情報</span></td>
				<td align="right" id="title1"><span onclick="event_close('1')" style="CURSOR:pointer;color:#ffffff;font-size:11px;">×閉じる</span></td>
			</tr>
			<tr bgcolor="#ffffff">
				<td colspan="2" id="box1">$reload</td>
			</tr>
		</table>
EOM
	}

	print "<table width=100% border=0 cellspacing=10 cellpadding=0>";
	
	#参加者表示
	if ($sanka_hyouzi_kinou == 1){
		open(GUEST,"< $guestfile");
		eval{ flock (GUEST, 1); };
		@all_guest=<GUEST>;
		close(GUEST);
		$genzai_zikoku = time;
		$genzaino_ninzuu = @all_guest;
        
		$sanka_kanri=0;
		foreach (@kanri_name){
			if($name eq "$_"){$sanka_kanri=1;last;}
		}
		
		$sanka_flag=0;
		@new_all_guest = ();
		foreach (@all_guest) {
			($sanka_timer,$sanka_name,$hyouzi_check,$mati_name) = split(/<>/);
			if ($name eq "$sanka_name"){
				if ($in{'sanka_hyouzi_on'}){$hyouzi_check = "$in{'sanka_hyouzi_on'}";}
				$sanka_flag=1;
				$sanka_timer = $genzai_zikoku;
				$mati_name = $in{'town_no'};
			}
			if( $genzai_zikoku - $logout_time > $sanka_timer){next;}
			chomp $mati_name;
			$sanka_tmp = "$sanka_timer<>$sanka_name<>$hyouzi_check<>$mati_name<>\n";
			push (@new_all_guest,$sanka_tmp);
		    
			if($mati_name ne ""){
				$sanka_mati = "$town_hairetu[$mati_name]にいます。";
			}else{
				$sanka_mati = "どこにいるか分かりまへんのや！";
			}
			&byou_hiduke($sanka_timer);
			if ($hyouzi_check eq "on"){
				$sanka_hyouzi .= "<a onMouseOver=\"Navi('$img_dir/para.gif', '参加者', '最終更新：$bh_full_date<br>$sanka_mati', 0, event);\" onMouseOut=\"NaviClose();\"><font $neme_back>$sanka_name</font></a><font size=1 color=#FF7F50>★</font>";
			}elsif ($name_disp && $sanka_kanri==1){
				$sanka_hyouzi .= "<a onMouseOver=\"Navi('$img_dir/para.gif', '参加者', '最終更新：$bh_full_date<br>$sanka_mati', 0, event);\" onMouseOut=\"NaviClose();\"><font color=$name_disp $neme_back>$sanka_name</font></a><font size=1 color=#FF7F50>★</font>";
			}
		}
	    
		if ($sanka_flag == 0 && $in{'mode'} ne ""){
			if ($genzaino_ninzuu >= $douzi_login_ninzuu && $in{'iiyudane'} eq ""){&error("現在、同時ログイン制限$douzi_login_ninzuu人を超えています。恐れ入りますが、しばらくしてからログインしてください。");}
       
			if ($in{'sanka_hyouzi_on'}){
				push(@new_all_guest,"$genzai_zikoku<>$name<>$in{'sanka_hyouzi_on'}<>$in{'town_no'}<>\n");
          
				if ($in{'sanka_hyouzi_on'} eq "on"){
					$sanka_hyouzi .= "<a onMouseOver=\"Navi('$img_dir/para.gif', '参加者', '最終更新：$bh_full_date<br>$sanka_mati', 0, event);\" onMouseOut=\"NaviClose();\"><font $neme_back>$name</font></a><font size=1 color=#FF7F50>★</font>";
				}elsif ($name_disp && $sanka_kanri==1){
					$sanka_hyouzi .= "<a onMouseOver=\"Navi('$img_dir/para.gif', '参加者', '最終更新：$bh_full_date<br>$sanka_mati', 0, event);\" onMouseOut=\"NaviClose();\"><font color=$name_disp $neme_back>$name</font></a><font size=1 color=#FF7F50>★</font>";
				}
			}else{
				push(@new_all_guest,"$genzai_zikoku<>$name<>$mise_type<>$in{'town_no'}<>\n");
				if ($mise_type eq "on"){
					$sanka_hyouzi .= "<a onMouseOver=\"Navi('$img_dir/para.gif', '参加者', '最終更新：$bh_full_date<br>$sanka_mati', 0, event);\" onMouseOut=\"NaviClose();\"><font $neme_back>$name</font></a><font size=1 color=#FF7F50>★</font>";
				}elsif ($name_disp && $sanka_kanri==1){
					$sanka_hyouzi .= "<a onMouseOver=\"Navi('$img_dir/para.gif', '参加者', '最終更新：$bh_full_date<br>$sanka_mati', 0, event);\" onMouseOut=\"NaviClose();\"><font color=$name_disp $neme_back>$name</font></a><font size=1 color=#FF7F50>★</font>";
				}
			}
		}


		if ($mem_lock_num == 0){
			$err = &data_save($guestfile, @new_all_guest);
			if ($err) {&error("$err");}
		}else{
			&lock;	
			open(GUEST,">$guestfile");
			eval{ flock (GUEST, 2); };
			print GUEST @new_all_guest;
			close(GUEST);
			&unlock;
		}
    
		$sankaninzuu = @new_all_guest;
		if ($sanka_hyouzi_iti == 1){
			print <<"EOM";
			<tr><td colspan=2>
			<font size=2 color=#333333 $neme_back>現在の総参加者(<B>$sankaninzuu人</B>)：</font><!-- koko 2005/04/06 -->
			$sanka_hyouzi
			</td></tr>
EOM
		}
	}
	
	my @filesize_check = stat($logfile);
	if ($filesize_check[7] > 600000){&error("$logfileの容量に問題があります。管理者（$master_ad）までお知らせください。");}

	my @filesize_check = stat($logfile);
	if ($filesize_check[7] > 600000){&error("$logfileの容量に問題があります。管理者（$master_ad）までお知らせください。");}
	
#ヘルプウインドウ
	print <<"EOM";
	<tr><td width="522" valign=top>
		<table background="$takasi_bak" border="0" cellspacing="0" cellpadding="0" style="background-color:$sotonoiro;">
		<tr valign="center" style="$page_back[$this_town_no]"> 
		<td height="8" width="8"  align=center> </td>
EOM

#ヨコの番号部分出力
	foreach $yokoziku_koumoku (1..16) {
		print "<td height=8 width=32 align=center class=migi style=color:$mojisyoku[$in{'town_no'}];>$yokoziku_koumoku</td>";
	}
	print "</tr>";
	
#ヨコの番号(td)の数だけタテの記号(tr)を出力
	$i = 21;
	foreach $tateziku_kigou  (A..L) {
		print "<tr valign=center><td height=32 width=8 style=\"$page_back[$this_town_no]\" align=center class=sita style=color:$mojisyoku[$in{'town_no'}];>$tateziku_kigou</td>\n";
		foreach $yokoziku_bangou (1..16) {
			($town_sprit_matrix[$yokoziku_bangou + $i],$akichi) = split(/=/,$town_sprit_matrix[$yokoziku_bangou + $i]);
			if ($town_sprit_matrix[$yokoziku_bangou + $i]){
				print "$unit{$town_sprit_matrix[$yokoziku_bangou + $i]}\n";
			}else{print "<td height=32 width=32></td>\n";}
		}
		print "</tr>\n";
		$i += 17;
	}
	print "</table>\n";
	
	#ログイン画面の表示
	if($in{'mode'} eq "login_view"){
		#アンケートを表示
		open(EN,"$enq_all") || &error("open Error : $enq_all");
		eval "flock(EN, 2);";
		@all_data=<EN>;
		close(EN);
		
		$enq_rand = int(rand(@all_data));
		($enq_id,$enq_title,$enq_name,$enq_kazu,$enq_ninzuu,$enq_seigen,$enq_special)=split(/<>/,$all_data[$enq_rand]);
		if(!$enq_special and int(rand(2))+1 == 1){
			$enq_rand2 = int(rand(@all_data));
			($enq_id,$enq_title,$enq_name,$enq_kazu,$enq_ninzuu,$enq_seigen,$enq_special)=split(/<>/,$all_data[$enq_rand2]);
		}
		
		$enq_mem="member/$enq_id/enq_member.cgi";
		open(OUT,"$enq_mem") || &error("open Error : $enq_mem");
		@enq_data=<OUT>;
		foreach(@enq_data){
			chomp ($_);
			if($_ eq $name){
				$sudeni = "<br><br><font color=\"red\"><b>（※既に投稿しています。）</b></font>";
				$select_able = "disabled";
				$submit_able = "disabled";
				$text_able = "disabled";
				last;
			}
		}
		close(OUT);
		
		$enq_data="member/$enq_id/enq_data.cgi";
		open(OUT,"$enq_data") || &error("open Error : $enq_data");
		@enq_data=<OUT>;
		foreach(@enq_data){
			($sentaku,$kazu)=split(/<>/);
			$all_kazu += $kazu;
		}
		foreach(@enq_data){
			($sentaku,$kazu)=split(/<>/);
			if($all_kazu){
				$enq_width = int(($kazu / $all_kazu)*250);
			}
			$printenq .= <<"EOM";
			<tr>
			<td><input type="radio" name="sentaku" value="$sentaku" id="$sentaku" $select_able><label for="$sentaku">$sentaku</label></td>
			<td><img src="$img_dir/energy_ao.gif" width="$enq_width" height="8">（$kazu票）</td>
			</tr>
EOM
		}
		close(OUT);
		
		$enq_table .= <<"EOM";
$enq_nameさんのアンケート<br>
<b>$enq_title</b>$sudeni
<hr>
<form action="enq.cgi" method="POST">
<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>write<>">
<input type=hidden name=enq_id value="$enq_id">
<input type=hidden name=enq_name value="$enq_name">
<input type=hidden name=enq_title value="$enq_title">

<table cellpadding="3" cellspacing="0" border="1" width="95%" align="center">
<tr bgcolor="#999999" align="center"><td width="50%">
	<font color="#ffffff"><b>選択肢</b></font>
</td>
<td width="50%">
	<font color="#ffffff"><b>投票数</b></font>
</td>
</tr>
	$printenq
<tr>
<td colspan="2">
	<input type="radio" name="sentaku" id="sentaku" value="" $select_able><label for="sentaku">その他（選択肢追加）</label>
	<input type="text" name="enq_tuika" size="50" $text_able>
</td>
</tr>
</table>
<br>
<center><input type="submit" value="投票するで" $submit_able></center>

</form>
EOM
		
		#あいさつを表示
		if ($top_aisatu_hyouzi == 1){
			open(IN,"$aisatu_logfile") || &error("Open Error : $aisatu_logfile");
			eval{ flock (IN, 2); };
			@aisatu_data = <IN>;
			close(IN);
			
			#あいさつ画面上部
			if (@aisatu_data ne ""){
				$aisatu_syurui .= "<option value=\"ノーマル\">ノーマル</option>\n";
				$aisatu_syurui .= "<option value=\"ジャンケン\">ジャンケン</option>\n";
				$aisatu_syurui .= "<option value=\"宣伝\" STYLE=\"color:#0000ff;\">宣伝</option>\n";
				if ($name eq $admin_name){
					$aisatu_syurui .= "<option value=\"管理人\" STYLE=\"color:#ff0000;\">管理人</option>\n";
				}
				foreach (@kanri_name){
					if($name eq "$_" and $name ne $admin_name){
						$aisatu_syurui .= "<option value=\"副管理人\" STYLE=\"color:#ff0000;\">副管理人</option>\n";
                    }
				}

				$aisatu_table .= "<table border=0 bgcolor=#ffffff width=\"522px\" align=left cellspacing=0 cellpadding=0 id=\"T01\"><tr><td><table width=\"522px\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\" bgcolor=#ffffcc><tr><form method=\"POST\" action=\"$script\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>aisatu<>\"><th><label><input type=\"checkbox\" name=\"kansai\" value=\"on\">関西弁に翻訳</label><select name=a_syurui>$aisatu_syurui</select><a href=\"tag.cgi\" target=\"_blank\"><u><font color=\"red\">独自タグ作成</font></u></a><br><input type=text name=a_com size=\"80\"><input type=submit value=\"発言\"></th></form></tr></table></td></form></tr>";
			}
			$i=0;

			#あいさつ種類分け
			foreach (@aisatu_data){
				local($a_num,$a_name,$a_date,$a_com,$a_syurui,$ie_link)= split(/<>/);
				if ($a_syurui eq '管理人' || $a_syurui eq '副管理人'){
					push (@aisatu_kayrinin,$_);
				}elsif($a_syurui eq '宣伝'){
					push (@aisatu_senden,$_);
				}else{
					push (@aisatu_futsu,$_);
				}
			}

			#管理人メッセージ
			foreach (@aisatu_kayrinin){
				local($a_num,$a_name,$a_date,$a_com,$a_syurui,$ie_link,$jyan)= split(/<>/);
				chomp $ie_link;
				if ($ie_link){
					$aisatu_table2 .= "<hr><form method=POST action=\"original_house.cgi\" style=\"margin: 0px 0px 0px 0px;\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>houmon<>\">$ie_link<input type=image src=\"./img/house_mini.gif\"><span style=\"color:$top_aisatu_hyouzi_iro1;\">$a_name：</span><span  style=\"color:$top_aisatu_hyouzi_iro2;\">$a_com$a_date</span></form>";
				}else{
					$aisatu_table2 .= "<hr><span style=\"color:$top_aisatu_hyouzi_iro1;\">$a_name：</span><span style=\"color:$top_aisatu_hyouzi_iro2;\">$a_com$a_date</span>";
				}
			}
			
			#宣伝
			foreach (@aisatu_senden){
				local($a_num,$a_name,$a_date,$a_com,$a_syurui,$ie_link,$jyan)= split(/<>/);
				chomp $ie_link;
				if ($ie_link){
					$aisatu_table3 .= "<hr><form method=POST action=\"original_house.cgi\" style=\"margin: 0px 0px 0px 0px;\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>houmon<>\">$ie_link<input type=image src=\"./img/house_mini.gif\"><span style=\"color:$top_aisatu_hyouzi_iro1;\">$a_name：</span><span  style=\"color:$top_aisatu_hyouzi_iro2;\">$a_com$a_date</span></form>";
				}else{
					$aisatu_table3 .= "<hr><span style=\"color:$top_aisatu_hyouzi_iro1;\">$a_name：</span><span style=\"color:$top_aisatu_hyouzi_iro2;\">$a_com$a_date</span>";
				}
			}
			
			#普通
			foreach (@aisatu_futsu){
				local($a_num,$a_name,$a_date,$a_com,$a_syurui,$ie_link,$jyan)= split(/<>/);
				chomp $ie_link;
				if ($ie_link){
					$aisatu_table .= "<tr><form method=POST action=\"original_house.cgi\" style=\"margin: 0px 0px 0px 0px;white-space:noemal;\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>houmon<>\"><td onMouseOver=\"Navi('$img_dir/aisatu.gif', '$a_syurui', '$jyan$a_date', 0, event);Aisatu_on(this);\" onMouseOut=\"NaviClose();Aisatu_out(this);\">$ie_link<input type=image src=\"./img/house_mini.gif\"><span style=\"color:$top_aisatu_hyouzi_iro1;\">$a_name：</span><span style=\"color:$top_aisatu_hyouzi_iro2;\">$a_com</span></td></form></tr>\n";
				}else{
					$aisatu_table .= "<tr style=\"white-space:noemal;\"><td onMouseOver=\"Navi('$img_dir/aisatu.gif', '$a_syurui', '$jyan$a_date', 0, event);Aisatu_on(this);\" onMouseout=\"NaviClose();Aisatu_out(this);\"><span style=\"color:$top_aisatu_hyouzi_iro1;\">$a_name：</span><span style=\"color:$top_aisatu_hyouzi_iro2;\">$a_com</span></td></tr>";
				}
				$i ++;
				if ($i >= $top_aisatu_hyouzikensuu){last;}
			}
			
			#あいさつ下部
			if (@aisatu_data ne ""){
				$aisatu_table .= "<tr><th><form method=\"POST\" action=\"yakuba.cgi\" style=\"margin: 0px 0px 0px 0px;\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>yakuba<>\"><input type=\"hidden\" name=\"sortid\" value=\"iu\"><input type=submit value=挨拶ログ一覧 style=\"border:1px solid;\"></th></form></tr></table>";
			}
			
			#実際に表示
			print <<"EOM";
			
<SCRIPT type="text/javascript" language="JavaScript"><!--
	function Aisatu_on(place){
		place.style.backgroundColor = '#FFC87D';
		place.style.fontSize = $fontsize+1;
		place.style.fontWeight = 'bold';
	}
	function Aisatu_out(place){
		place.style.backgroundColor = '';
		place.style.fontSize = $fontsize;
		place.style.fontWeight = '';
	}
--></script>
$aisatu_table
EOM
		}
		
	}else{
		#ログイン画面じゃないとき
		print "$top_information";
	}

	print "</td><td valign=top>";

	#右側の画面
	if ($in{'mode'} eq ""){
		&top_gamen;
	}elsif ($in{'mode'} eq "kentiku_do" && $in{'command'} eq "kakunin"){
		&kentiku_kakunin;
	}else{
		&town_jouhou($this_town_no);
		&loged_gamen;
	}
	
	if ($sanka_hyouzi_kinou == 1 && $sanka_hyouzi_iti == 0){
		print <<"EOM";
		</td></tr>
		<tr><td colspan=2>
		<font size=2 color=#333333 $neme_back>現在の総参加者(<B>$sankaninzuu人</B>)：</font>
		$sanka_hyouzi
EOM
	}
    
	print "</td></tr></table>";
	
	&hooter("","");
}

####建築確認画面
sub kentiku_kakunin {
	if ($in{'iegazou'} eq ""){&error("家の画像が選択されていません");}
	unless ($in{'matirank'} eq "" || $in{'tuika'} eq ""){&error("家のランクが選択されていません");}
	$ori_ie_image = "$img_dir/$in{'iegazou'}";
	if ($in{'matirank'} eq "0"){$kauieno_rank = "A";}
	elsif  ($in{'matirank'} eq "1"){$kauieno_rank = "B";}
	elsif  ($in{'matirank'} eq "2"){$kauieno_rank = "C";}
	elsif  ($in{'matirank'} eq "3"){$kauieno_rank = "D";}
	elsif  ($in{'tuika'} eq "0"){$kauieno_rank = "家のみ";}
	elsif  ($in{'tuika'} eq "1"){$kauieno_rank = "運営";}
	elsif  ($in{'tuika'} eq "2"){$kauieno_rank = "株式会社";}
	elsif  ($in{'tuika'} eq "3"){$kauieno_rank = "持ち物販売所";}

	if ($in{'ie_nedan'}){$ie_hash{$in{'iegazou'}} *= $in{'ie_nedan'}};

#金額計算
	if ($in{'matirank'} ne ""){
		$kensetu_hiyou = $town_tika_hairetu[$in{'mati_sentaku'}] + $ie_hash{$in{'iegazou'}} + $housu_nedan[$in{'matirank'}];
		$hojyo_nedan = $housu_nedan[$in{'matirank'}];
	}else{
		$kensetu_hiyou = $town_tika_hairetu[$in{'mati_sentaku'}] + $ie_hash{$in{'iegazou'}} + $housu_tuika2[$in{'tuika'}];
		$hojyo_nedan = $housu_tuika2[$in{'tuika'}];
	}
    
	if(!$k_id){&error("mono.cgi エラー command")}
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,"< $monokiroku_file") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 1); };
	@my_kounyuu_list =<OUT>;
	close(OUT);
	foreach (@my_kounyuu_list){
		&syouhin_sprit ($_);
		if ($syo_kouka eq "クレジット"){
			if ($syo_taikyuu - (int ((time - $syo_kounyuubi) / (60*60*24)))){
				$siharai_houhou .= "<option value=\"$syo_hinmoku\">$syo_hinmoku</option>";
			}
		}
	}
	
	print <<"EOM";
<table width="100%" border="0" cellspacing="0" cellpadding="7" class=yosumi><tr><td>
<div align=center class=dai>建 築 仕 様 書</div><hr size=1><br>
<div class=tyuu>建築する街</div>
$town_hairetu[$in{'mati_sentaku'}]（地価：$town_tika_hairetu[$in{'mati_sentaku'}]万円）<br><br>
<div class=tyuu>場所</div>
左の<img src ="$img_dir/kentiku_yotei.gif" width=32 height=32 border=0 align=middle>の位置に建てられます。<br><br>
<div class=tyuu>家（外装）</div>
<img src="$ori_ie_image" width=32 height=32> （$ie_hash{$in{'iegazou'}}万円）<br><br>
<div class=tyuu>家（内装）</div>
$kauieno_rank（価格：$hojyo_nedan万円）<br><br>
<div class=job_messe>建築費用は<br>
<div class=dai>$kensetu_hiyou 万円</div>
となります。</div>

<form method="POST" action="$script">

	
	<input type=hidden name=ori_k_id value="$k_id">
	<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>kentiku_do<>">
	<input type=hidden name=ori_ie_town value="$in{'mati_sentaku'}">
	<input type=hidden name=ori_ie_sentaku_point value="$sentaku_point">
	<input type=hidden name=ori_ie_tateziku value="$in{'tateziku'}">
	<input type=hidden name=ori_ie_yokoziku value="$in{'yokoziku'}">
	<input type=hidden name=ori_ie_image value="$ori_ie_image">
	<input type=hidden name=ori_ie_rank value="$in{'matirank'}">
	<input type=hidden name=ori_ie_tuika value="$in{'tuika'}">
	<input type=hidden name=kensetu_hiyou value="$kensetu_hiyou">
	<div align=center>
	支払い方法 <select name="siharaihouhou"><option value="現金">現金</option>$siharai_houhou</select><br>
	<input type="submit"value="この内容で家を建てる"><br><br>
	<a href=\"javascript:history.back()\"> [前の画面に戻る] </a></div>
</form>

</td></tr></table>
EOM
}

########### 有料ジャンプ
sub jamp_url{

    open(IN,"log_dir/ranking.cgi") || &error("open Error : log_dir/ranking.cgi");
	eval "flock(IN, 2);";
	@member=<IN>;
	close(IN);
    
    ($mae_name,$mae_time)=split(/<>/,$member[0]);
    ($m_sec,$m_min,$m_hour,$m_day,$m_mon,$m_year,$m_week)=localtime($mae_time);
    $m_mon+=1;
    ($sec,$min,$hour,$day,$mon,$year,$week)=localtime(time);
    $mon+=1;
        
    $time=time;
    
    if($m_day!=$day or $m_mon!=$mon or $m_year!=$year){
    open(AL,"+> log_dir/ranking.cgi") || &error("open Error : log_dir/ranking.cgi");
	eval "flock(AL, 2);";
	close(AL);
    open(AL,"> log_dir/ranking.cgi") || &error("open Error : log_dir/ranking.cgi");
    eval "flock(AL, 2);";
	print AL "$name<>$time<>\n";
    close(AL);
    }else{
    	foreach(@member){
    	($j_name,$j_time)=split(/<>/);
    	    	if($j_name eq $name){
    	    	&error("1日1回でっせ");
    	    	}
    	}
    unshift @member,"$name<>$time<>\n";
    open(IN,"+< log_dir/ranking.cgi") || &error("open Error : log_dir/ranking.cgi");
	eval "flock(IN, 2);";
	seek(IN, 0, 0);
	print IN @member;
	truncate(IN, tell(IN));
	close(IN);
	
    }
    
	$url_adresu = 'http://game.atmk.in/cgi_game/rc.php?s=town&id=4-Ik9n';
	$url_adresu2 = 'http://www.seijyuu.com/game/link/in.cgi?kind=town&id=tyage';
	
	$money += 10000;
	$kpoint += 1;
	#ログ更新
	&temp_routin;
	&log_kousin($my_log_file,$k_temp);

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
	print <<"EOM";
<html>
<head>
<META http-equiv="content-type" content="text/html; charset=Shift_JIS">
<script type="text/javascript"><!-- 
window.open("$url_adresu","_blank");
window.open("$url_adresu2","_self");
 --></script>
</head>
<h2 align=center><font color=\"red\">10000円ゲットしました。<br>評価ポイントが１Ｐあがりました。</font></h2>
</body></html>
EOM
	exit;
}

1;