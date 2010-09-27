#!/usr/bin/perl
#↑お使いのサーバーのパスにあわせてください。
#####################
#"広告" => "<form method=POST action=\"koukoku.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>top<>\"><td height=32 width=32><input type=image src='$img_dir/ad.gif' onMouseOver=\"Navi('$img_dir/ad.gif', '広告', '公共広告機関です。<br>街の人全員に宣伝を送ることができます。');\" onMouseOut=\"NaviClose();\"></td></form>",
#####################

$this_script = 'koukoku.cgi';
require './town_ini.cgi';
require './town_lib.pl';
require './unit.pl';
require './event.pl';
&decode;

#メンテチェック
	if($mente_flag == 1 && $in{'admin_pass'} eq "" && $in{'mode'} ne ""){&error("$mente_message")}
$seigenyou_now_time = time;
#制限時間チェック
		$ato_nanbyou=$koudou_seigen-($seigenyou_now_time - $access_byou);
		if($seigenyou_now_time - $access_byou < $koudou_seigen){&error("まだ行動できません。あと$ato_nanbyou秒お待ちください。")}
	
#条件分岐
	if($in{'mode'} eq "top"){&top;}
	elsif($in{'mode'} eq "dm"){&dm;}
	else{&error("「戻る」ボタンで街に戻ってください");}

############################top

sub top {
			&motimono_kensa_ev2("許可証");
			if ($kensa_flag != 1){&error("許可証が無いと入れません。<br>管理人からもらってください。");}


	&header(item_style);

	print <<"EOM";
<center>
<font color=red><font size=6>++公共広告機関++</font></font><hr>
<font size=3>$titleの全住民にメールを送信します。<br>全住民に送信するものですのでマナーを守りましょう</font><br>必ず管理人の許可をもらってから使用してください。<br>未許可のまま使用すると処罰の対象になります。
  			<form method="POST" action="$this_script">
			<input type=hidden name=mode value="dm">
			<input type=hidden name=sort_id value="0">
			<input type=hidden name=name value="$in{'name'}">
			<input type=hidden name=pass value="$in{'pass'}">
			<input type=hidden name=id value="$in{'id'}">
			<input type=hidden name=town_no value="$in{'town_no'}">
			<textarea name=isseimail rows=5 cols=80></textarea>
			<input type=submit value="送信">
			</form>
			協力：肉まんさん

EOM
	&hooter("login_view","戻る");
exit;
}

##############一斉メール#################koko2006/12/23
sub dm {
	$member_f = './log_dir/memberlog.cgi';
	open(IN,"$logfile") || &error("Open Error : $logfile");
	@member = <IN>;
	close(IN);

	$kanrisyaname = "$in{'name'}さん～公共広告機関～";

	
                $in{'isseimail'} = &tag($in{'isseimail'});
				$in{'isseimail'} =~ s/\r\n/<br>/g;
				$in{'isseimail'} =~ s/\r/<br>/g;
				$in{'isseimail'} =~ s/\n/<br>/g;
	&time_get;
	foreach (@member){
		(@member_list) = split(/<>/);
		$message_file = "./member/$member_list[0]/mail.cgi";

		open(AIT,"$message_file") || &error("お相手の方のメール記録ファイル（$message_file）が開けません。");
		$last_mail_check_time = <AIT>;
		@mail_cont = <AIT>;
		close(AIT);
		$new_mail = "受信<>$kanrisyaname<>$in{'isseimail'}<>$date2<>$date_sec<><><><><><>\n";
		unshift (@mail_cont,$new_mail);
		if (@mail_cont > $mail_hozon_gandosuu){pop @mail_cont;}	#ver.1.30
#最終メールチェック時間がなければ１を入れる
		if ($last_mail_check_time eq ""){$last_mail_check_time = "1\n";}
		unshift (@mail_cont,$last_mail_check_time);
#		&lock; #koko2006/10/18
		open(OUT,">$message_file") || &error("$message_fileに書き込めません");
		eval{ flock (OUT, 2); };
		print OUT @mail_cont;
		close(OUT);
#		&unlock; #koko2006/10/18
	}
	&header;
	print "<div align=center>\n";
	print "<br><br>以下の内容で送信完了しました。<br><br>\n";
	print "$in{'isseimail'}\n";
	print "<br><br><a href=\"javascript:history.back()\"> [前の画面に戻る] </a></div>\n";
	
	print "</body></html>\n";
	exit;
}
