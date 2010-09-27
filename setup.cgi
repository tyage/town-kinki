#!/usr/bin/perl

$this_script = 'setup.cgi';

require './town_ini.cgi';
require './town_lib.pl';

&decode;

#=====　メンテチェック　=====#
if($mente_flag == 1 && $in{'admin_pass'} eq "" && $in{'mode'} ne ""){&error("$mente_message")}

#=====　制限時間チェック　=====#
$seigenyou_now_time = time;
$ato_nanbyou=$koudou_seigen-($seigenyou_now_time - $access_byou);
if($seigenyou_now_time - $access_byou < $koudou_seigen){&error("まだ行動できません。あと$ato_nanbyou秒お待ちください。")}

#=====　条件分岐　=====#
if($in{'mode'} eq "setup"){&setup;}
elsif($in{'mode'} eq "change"){&change;}
elsif($in{'mode'} eq "friend"){&friend;}
elsif($in{'mode'} eq "memo"){&memo;}
elsif($in{'mode'} eq "die"){&die;}
else{&error("「戻る」ボタンで街に戻ってください");}

exit;

#--------------------
#トップ画面
#--------------------
sub setup{
	$friend_file="./member/$k_id/friend.cgi";
	if (-e $friend_file){
		open(IN,"<$friend_file") || &error("$friend_fileが開けません");
		eval{ flock (IN, 2); };
		@friend_data = <IN>;
		foreach(@friend_data){
			chomp $_;
			$friend_option .= "<option value=\"$_\">$_</option>\n";
		}
		close(IN);
	}
	
	$memo_file="./member/$k_id/memo.cgi";
	if (-e $memo_file){
		open(IN,"<$memo_file") || &error("$memo_fileが開けません");
		eval{ flock (IN, 2); };
		$memo_data = <IN>;
		$memo_data =~ s/<br>/\n/g;
		close(IN);
	}
	
	if($oto eq 'on'){$checked_on = "checked";}
	
	if($fontsize eq "16"){$select0 = "selected";}
	elsif($fontsize eq "15"){$select1 = "selected";}
	elsif($fontsize eq "14"){$select2 = "selected";}
	elsif($fontsize eq "13"){$select3 = "selected";}
	elsif($fontsize eq "12"){$select4 = "selected";}
	elsif($fontsize eq "11"){$select5 = "selected";}
	elsif($fontsize eq "10"){$select6 = "selected";}

	&header(item_style);
	print <<"EOM";
<table width="90%" border="0" cellspacing="0" cellpadding="10" align="center" class="yosumi">
<tr>
<td>
	ここではあなたの設定や、死亡届を出すことなどができます。<br>
</td>
<td bgcolor="#333333" align=center width="300">
	<font color="#ffffff" size="5"><b>マイ設定</b></font>
</td>
</tr>
</table>
<br>
<br>
<table width="90%" border="0" cellspacing="0" cellpadding="10" align="center" bgcolor="#ffffff" style="border:1px solid #000000;">
<tr>
<td>
	<span style="color:red;">■アンケート一覧</span><br>
	<br>
	<form action="$this_script" method="POST">
	<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>change<>">
	<label for="pass">パスワード変更</label>　<input type="text" name="pass_change" size="20" value="$pass" id="pass"><br>
	<br>
	<input type=checkbox name=otodashi value="on" id="otodashi" $checked_on><label for="otodashi">音を出す（リロード時）</label><br>
	<br>
	文字サイズ変更　
	<select name="size">
	<option value="16" $select0>ごっさでかい（極大）</option>
	<option value="15" $select1>どでかい（特大）</option>
	<option value="14" $select2>おおきい（大）</option>
	<option value="13" $select3>ちゅーくらい（中）</option>
	<option value="12" $select4>ちいさい（小）</option>
	<option value="11" $select5>ちっこい（特小）</option>
	<option value="10" $select6>めっさちっさい（極小）</option>
	</select><br>
	<br>
	<input type="submit" value="設定変更">
	</form>
</td>
</tr>
</table>
<br>
<table width="90%" border="0" cellspacing="0" cellpadding="10" align="center" bgcolor="#ffffff" style="border:1px solid #000000;">
<tr>
<td>
	<span style="color:red;">■移動に使うもの</span><br>
	<br>
	
</td>
</tr>
</table>
<br>
<table width="90%" border="0" cellspacing="0" cellpadding="10" align="center" bgcolor="#ffffff" style="border:1px solid #000000;">
<tr>
<td>
	<span style="color:red;">■友達リスト</span><br>
	<br>
	<form action="$this_script" method="POST">
	<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>friend<>">
	●リストから消去（Ctrlで複数消去）<br>
	<select size="5" multiple name="friend_data_delete">$friend_option</select><br>
	<br>
	●リストに追加（改行で複数追加）<br>
	<textarea cols="50" rows="5" name="friend_data_add"></textarea><br>
	<br>
	<input type="submit" value="内容を変更する">
	</form>
</td>
</tr>
</table>
<br>
<table width="90%" border="0" cellspacing="0" cellpadding="10" align="center" bgcolor="#ffffff" style="border:1px solid #000000;">
<tr>
<td>
	<span style="color:red;">■メモ帳</span><br>
	<br>
	<form action="$this_script" method="POST">
	<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>memo<>">
	<textarea cols="100" rows="10" name="memo_data">$memo_data</textarea><br>
	<br>
	<input type="submit" value="内容を変更する">
	</form>
</td>
</tr>
</table>
<br>
<table width="90%" border="0" cellspacing="0" cellpadding="10" align="center" bgcolor="#ffffff" style="border:1px solid #000000;">
<tr>
<td>
	<span style="color:red;">■死亡届</span><br>
	<br>
	<form action="$this_script" method="POST">
	<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>die<>">
	<span style="color:red;"><b>※死亡届を出すとデータが消えてしまいます！</b></span><br>
	<br>
	<input type="button" value="死亡届を出す" onclick="if( confirm('本当に出しますか？　※死亡届を出すとデータが消えてしまいます！！！') ){this.form.submit();}">
	</form>
</td>
</tr>
</table>
EOM
	
	&hooter("login_view","街に戻る");
	
	exit;
}

#--------------------
#ステータス変更
#--------------------
sub change{
	if(!$in{'pass_change'}){&error("パスワードを設定してください。");}
	$in{'pass'} = $in{'pass_change'};
	
	#=====　人生のゲームデータ修正　=====#
	#リストでのデータ
	$sugoroku_file = "./sugoroku/zinseilog.cgi";
	open(IN,"< $sugoroku_file") || &error("Open Error : $sugoroku_file");
	eval{flock(IN,2);};
	@sugoroku_data = <IN>;
	close(IN);
	
	$sugoroku_flag = "off";
	foreach(@sugoroku_data){
		($s_id,$s_name,$s_pass,$s_money,$s_basyo,$s_haiguu,$s_kodomo,$s_love,$s_land,$s_house,$s_kabu,$s_kounyuu,$s_sex,$s_yobi1,$s_yobi2,$s_yobi3,$s_yobi4,$s_yobi5,$s_yobi6,$s_yobi7,$s_yobi8,$s_yobi9,$s_yobi10,$s_yobi11,$s_yobi12,$s_yobi13,$s_yobi14)= split(/<>/);
		if($s_id eq $in{'name'}){
			$sugoroku_id = $s_id;
			$s_pass = $in{'pass_change'};
			$sugoroku_flag = "on";
		}
		$my_temp="$s_id<>$s_name<>$s_pass<>$s_money<>$s_basyo<>$s_haiguu<>$s_kodomo<>$s_love<>$s_land<>$s_house<>$s_kabu<>$s_kounyuu<>$s_sex<>$s_yobi1<>$s_yobi2<>$s_yobi3<>$s_yobi4<>$s_yobi5<>$s_yobi6<>$s_yobi7<>$s_yobi8<>$s_yobi9<>$s_yobi10<>$s_yobi11<>$s_yobi12<>$s_yobi13<>$s_yobi14<>\n";
		push(@new_sugoroku_data,$my_temp);
	}
	
	if($sugoroku_flag eq "on"){
		open(OUT,"> $sugoroku_file") || &error("Write Error : $sugoroku_file");
		print OUT @new_sugoroku_data;
		close(OUT);
		
		#個人ファイルのデータ
		$sugoroku_my_file = "./sugoroku/member/{$sugoroku_id}log.cgi";
		open(IN,"< $sugoroku_my_file") || &error("Open Error : $sugoroku_my_file");
		eval{flock(IN,2);};
		$sugoroku_data = <IN>;
		close(IN);
		
		($s_id,$s_name,$s_pass,$s_money,$s_basyo,$s_haiguu,$s_kodomo,$s_love,$s_land,$s_house,$s_kabu,$s_kounyuu,$s_sex,$s_yobi1,$s_yobi2,$s_yobi3,$s_yobi4,$s_yobi5,$s_yobi6,$s_yobi7,$s_yobi8,$s_yobi9,$s_yobi10,$s_yobi11,$s_yobi12,$s_yobi13,$s_yobi14)= split(/<>/,$sugoroku_data);
		$s_pass = $in{'pass_change'};
		$my_temp="$s_id<>$s_name<>$s_pass<>$s_money<>$s_basyo<>$s_haiguu<>$s_kodomo<>$s_love<>$s_land<>$s_house<>$s_kabu<>$s_kounyuu<>$s_sex<>$s_yobi1<>$s_yobi2<>$s_yobi3<>$s_yobi4<>$s_yobi5<>$s_yobi6<>$s_yobi7<>$s_yobi8<>$s_yobi9<>$s_yobi10<>$s_yobi11<>$s_yobi12<>$s_yobi13<>$s_yobi14<>\n";
		
		open(OUT,"> $sugoroku_file") || &error("Write Error : $sugoroku_file");
		print OUT $my_temp;
		close(OUT);
	}
	
	#=====　リストデータ修正　=====#
	open(IN,"< $logfile") || &error("Open Error : $logfile");
	eval{ flock (IN, 2); };
	@rankingMember = <IN>;
	close(IN);
	
	$sonzai_flag=0;
	
	@new_ranking_data = ();
	foreach (@rankingMember) {
		&list_sprit($_);
		if ($list_name eq $in{'name'}){
			$sonzai_flag=1;
			$list_pass = $in{'pass_change'};
			$list_oto = $in{'otodashi'};
			$list_fontsize = $in{'size'};
		}
		&list_temp;
		push (@new_ranking_data,$list_temp);
	}
	if ($sonzai_flag == 0){&error("リストにあなたの参加者が見つかりません");}
	
	#=====　個人データ修正　=====#
	$my_log_file = "./member/$in{'k_id'}/log.cgi";
	open(MYL,"< $my_log_file")|| &error("Open Error : $my_log_file");
	eval{ flock (MYL, 2); };
	$my_prof = <MYL>;
	&kozin_sprit2($my_prof);
	close(MYL);
	
	$pass = $in{'pass_change'};
	$oto = $in{'otodashi'};
	$fontsize = $in{'size'};
	
	&temp_routin;
	&log_kousin($my_log_file,$k_temp);
	
	&lock;
	
	if ($mem_lock_num == 0){
		$err = &data_save($logfile, @new_ranking_data);
		if ($err) {&error("$err");}
	}else{
		open(OUT,">$logfile") || &error("Write Error : $logfile");
		eval{ flock (OUT, 2); };
		print OUT @new_ranking_data;
		close(OUT);
	}
	
	&unlock;
	
	&message("データを変更しました。","setup",$this_script);
}

#--------------------
#友達帳
#--------------------
sub friend{
	$friend_file="./member/$k_id/friend.cgi";
	if (! -e $friend_file){
		open(ME,">$friend_file") || &error("Write Error : $friend_file");
		eval{ flock (ME, 2); };
		chmod 0666,"$friend_file";
		close(ME);
	}
	
	open(IN,"< $friend_file") || &error("Open Error : $friend_file");
	eval{ flock (IN, 2); };
	@friend_data = <IN>;
	close(IN);
	
	if($in{'friend_data_delete'}){
		@friend_data_delete = split(/<>/,$in{'friend_data_delete'});
		foreach(@friend_data_delete){
			$friend_delete{$_} = "delete";
		}
	}
	
	foreach(@friend_data){
		chomp $_;
		if($friend_delete{$_}){next;}
		$friend{$_} = "allive";
		push(@new_friend_data,"$_\n");
	}
	
	if($in{'friend_data_add'}){
		open(IN,"< $logfile") || &error("Open Error : $logfile");
		eval{ flock (IN, 2); };
		@all_sankasya = <IN>;
		foreach (@all_sankasya) {
			&aite_sprit($_);
			$villager{$aite_name} = "allive";
		}
		close(IN);
	    
		@friend_data_add = split(/<br>/,$in{'friend_data_add'});
		foreach(@friend_data_add){
			if($_ eq ""){next;}
			if($friend{$_}){next;}
			if($villager{$_} eq ""){next;}
			$friend{$_} = "allive";
			push(@new_friend_data,"$_\n");
		}
	}
	
	open(OUT,">$friend_file") || &error("$friend_fileが開けません");
	eval{ flock (OUT, 2); };
	print OUT @new_friend_data;
	close(OUT);
	
	&message("友達帳の内容を変更しました。","setup",$this_script);
}

#--------------------
#メモ帳
#--------------------
sub memo{
	$memo_file="./member/$k_id/memo.cgi";
	if (! -e $memo_file){
		open(ME,">$memo_file") || &error("Write Error : $memo_file");
		eval{ flock (ME, 2); };
		chmod 0666,"$memo_file";
		close(ME);
	}
	
	open(OUT,">$memo_file") || &error("$memo_fileが開けません");
	eval{ flock (OUT, 2); };
	print OUT $in{'memo_data'};
	close(OUT);
	
	&message("メモ帳の内容を変更しました。","setup",$this_script);
}

#--------------------
#死亡届
#--------------------
sub die{
	if($in{'command'} eq "die"){
		if ($sanka_hyouzi_kinou == 1){
			open(GUEST,"< $guestfile");
			eval{ flock (GUEST, 1); };
			@all_guest=<GUEST>;
			close(GUEST);
	        
			@new_all_guest = ();
			foreach (@all_guest) {
				($sanka_timer,$sanka_name,$hyouzi_check,$mati_name) = split(/<>/);
				if ($name eq "$sanka_name"){next;}
				if( $genzai_zikoku - $logout_time > $sanka_timer){next;}
				chomp $mati_name;
				$sanka_tmp = "$sanka_timer<>$sanka_name<>$hyouzi_check<>$mati_name<>\n";
				push (@new_all_guest,$sanka_tmp);
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
		}
			
		if($pass ne $in{'pass_input'}){&error("パスワードが間違ってまっせ");}
		&lock;
		
		open(IN,"< $logfile") || &error("Open Error : $logfile");
		eval{ flock (IN, 1); };
		@rankingMember = <IN>;
		close(IN);
		@alldata = ();
		foreach (@rankingMember) {
			&list_sprit($_);
			if($list_name eq $name && $in{'pass_input'} eq $list_pass){
				#家削除処理
				&ie_sakujo_syori ($list_name);
				#アンケート削除処理
				&enq_sakujo_syori ($list_name);
				#結婚削除処理
				&kekkon_sakujo($list_name);
				#プロフィール＆結婚斡旋所削除処理
				&prof_sakujo2 ($list_name);
				&as_prof_sakujo2($list_name);
				
				#フォルダー内のファイル名を取得して削除。個人フォルダーの削除
				$sakujo_folder_id = "./member/$list_k_id";
				if (-e "$sakujo_folder_id") {
					use DirHandle;
					$dir = new DirHandle ("./member/"."$list_k_id");
					while($file_name = $dir->read){
						unlink ("./member/$list_k_id/$file_name");
					}
					$dir->close;
					rmdir("./member/$list_k_id") || &error("ID番号$list_k_idの$list_nameさんのデータ削除ができません");
				}
				&news_kiroku("転居","$list_nameさんが街を去りました。");
				
				next;
			}
			$data=$_;
			
			push @alldata,$data;
		}
		
		if ($mem_lock_num == 0){
			$err = &data_save($logfile, @alldata);
			if ($err) {&error("$err");}
		}else{
			open(OUT,">$logfile") || &error("$logfileが開けません");
			eval{ flock (OUT, 2); };
			print OUT @alldata;
			close(OUT);
		}
		
		&unlock;
		
		&header(item_style);
		print <<"EOM";
<div align=center>
<table border=0 cellspacing="5" cellpadding="0" width="70%" style="$message_win"><tr><td>
死亡届を出しました。
</td></tr></table>
<br>
<form method=POST action="$script">
<input type=submit value="街に戻る">
</form>
</div>
EOM
		exit;
	}
	
	&header(item_style);
	print <<"EOM";
<div align=center>
<table border=0 cellspacing="5" cellpadding="0" width="70%" style="$message_win"><tr><td>
<br>
	<form action="$this_script" method="POST">
	<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>die<>">
	<input type="hidden" name="command" value="die">
	<span style="color:red;"><b>※死亡届を出すとデータが消えてしまいます！</b></span><br>
	パスワード再入力<input type="text" name="pass_input" size="20"><br>
	<input type="button" value="死亡届を出す" onclick="if( confirm('本当に出しますか？　※死亡届を出すとデータが消えてしまいます！！！') ){this.form.submit();}">
	</form>
</td></tr></table>
<br>
<form method=POST action="$this_script">
<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>setup<>">
<input type=submit value="戻る">
</form>
</div>
EOM

}
