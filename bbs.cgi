#!/usr/bin/perl

#--------------------------------------#
#           学報用掲示板          　　 #
#　これはチャゲによって作られました。　#
#　　　　結構苦労したんやで。     　　 #
#                                  　　#
#　　Copyright (c) 2008　チャゲ   　　 #
# 　 web：http://tyage.a.orn.jp/ 　　  #
# 　 mail：tyage2@nifmail.jp     　　  #
#--------------------------------------#

require './town_ini.cgi';
require './town_lib.pl';

&decode;
&header(syokudou_style);

if($in{'name'} ne $admin_name){
	$in{'message'} =~ s/</&lt;/g;
	$in{'message'} =~ s/>/&gt;/g;
}

if($in{'mode'} eq "submit"){&submit;}
elsif($in{'mode'} eq "hensyuu"){&hensyuu;}
elsif($in{'mode'} eq "delete"){&delete;}
else{&top;}

exit;

######################
#　以下サブルーチン　#
######################

################
#-----投稿-----#
################
sub submit{
	if($in{'command'} eq "new"){
		if(!$in{'title'}){&error("タイトルがありません！");}
		if(!$in{'name'}){&error("名前を書いてください。");}
		if(!$in{'message'}){&error("メッセージないよ。");}
		
		#===専用ログ===#
		if($in{'senyou'}){
			open(IN,"< log_dir/php_member.cgi") or &error("Open error");
			eval{ flock (IN, 1); };
			@php_mamber=<IN>;
			close(IN);
			
			foreach(@php_mamber){
				chomp $_;
				if($in{'name'} eq $_){$flag = 1;}
				last;
			}
			if(!$flag){&error("メンバー以外は見れません。");}
		}
		
		#===全体ログ更新===#
		open(IN,"< php/all_log.cgi") or &error("Open error");
		eval{ flock (IN, 1); };
		@data=<IN>;
		close(IN);
		
		($mae_no,$mae_title,$mae_name,$mae_pass,$mae_senyou,$mae_last,$mae_laster,$mae_res)=split(/<>/,$data[0]);
		if($mae_title eq $in{'title'}){&error("同じタイトルがありまっせ。");}
		$mae_no++;
		$now=time;
		unshift(@data,"$mae_no<>$in{'title'}<>$in{'name'}<>$in{'pass'}<>$in{'senyou'}<>$now<>$in{'name'}<>0<>\n");

		open(OUT,"> php/all_log.cgi") or &error("Write error");
		eval{ flock (OUT, 2); };
		print OUT @data;
		close(OUT);
		
		#===ログ作成===#
		open(IN,"> php/${mae_no}.cgi") || &error("Write Error: $new.dat");
		print IN "0<>$in{'name'}<>$in{'pass'}<>$in{'message'}<>$now<>\n";
		close(IN);
		
		chmod(0666, "php/${mae_no}.cgi");
		
		#===表示===#
		print <<"EOM";
		<center>
		<table border=0 cellspacing="5" cellpadding="0" width=300>
		<tr><td>
		<center><h3><font color=#ff3300>新しいスレッドを作成しました。</font></h3></center>
		</td></tr>
		</table>
		</center>
EOM
	}elsif($in{'command'} eq "Re"){
		if(!$in{'message'}){&error("メッセージがありません！");}
		if(!$in{'name'}){&error("名前を書いてください。");}
		
		#===ログ更新===#
		open(IN,"< php/$in{'bbs_no'}.cgi") or &error("Open error");
		eval{ flock (OUT, 1); };
		@data=<IN>;
		close(IN);
		
		$data_suu=@data-1;
		($mae_no,$mae_name,$mae_pass,$mae_message,$mae_time)=split(/<>/,$data[$data_suu]);
		if($mae_name eq $in{'name'} and $mae_message eq $in{'message'}){&error("二重投稿禁止でっせ");}
		$mae_no++;
		$now=time;
		push(@data,"$mae_no<>$in{'name'}<>$in{'pass'}<>$in{'message'}<>$now<>\n");
		
		open(OUT,"> php/$in{'bbs_no'}.cgi") or &error("Write error");
		eval{ flock (OUT, 2); };
		print OUT @data;
		close(OUT);
		
		#===全体ログ更新===#
		open(IN,"< php/all_log.cgi") or &error("Open error");
		eval{ flock (IN, 1); };
		@data=<IN>;
		close(IN);
		
		foreach(@data){
			($no,$title,$name,$pass,$senyou,$last,$laster,$res)=split(/<>/);
			if($no==$in{'bbs_no'}){
				$last=time;
				$laster=$in{'name'};
				chomp $res;
				$res++;
			}
			push(@new_data,"$no<>$title<>$name<>$pass<>$senyou<>$last<>$laster<>$res<>\n");
		}
		
		open(OUT,"> php/all_log.cgi") or &error("Write error");
		eval{ flock (OUT, 2); };
		print OUT @new_data;
		close(OUT);
		
		#===表示===#
		print <<"EOM";
		<center>
		<table border=0 cellspacing="5" cellpadding="0" width=300>
		<tr><td>
		<center><h3><font color=#ff3300>スレッドに投稿しました。</font></h3></center>
		</td></tr>
		</table>
		</center>
EOM
	}else{&error("なんじゃこりゃあ～！");}
	
	&hooter("top","トップへ","bbs.cgi");
    
	exit;
}

################
#-----編集-----#
################
sub hensyuu{
	if($in{'command'} eq "thread"){
		if($in{'bbs_pass'}){
			#===全体ログ更新===#
			open(IN,"< php/all_log.cgi") or &error("Open error");
			eval{ flock (IN, 1); };
			foreach(<IN>){
				($no,$title,$name,$pass,$senyou,$last,$laster,$res)=split(/<>/);
				if($in{'bbs_no'}==$no){
					if($pass){
						if($in{'pass'} ne $pass and $in{'pass'} ne $admin_pass){&error("パスワードがちが～う！");}
					}else{
						if($in{'pass'} ne $admin_pass){&error("このスレにはパスワードが設定されていません。");}
					}
					$title=$in{'title'};
					$name=$in{'name'};
					$senyou=$in{'senyou'};
					$flag="1";
				}
				push(@new_all_data,"$no<>$title<>$name<>$pass<>$senyou<>$last<>$laster<>$res<>\n");
			}
			if(!$flag){&error("隊長！そんなスレ見つかりません！");}
			close(IN);
			
			open(OUT,"> php/all_log.cgi") or &error("Write error");
			eval{ flock (OUT, 2); };
			print OUT @new_all_data;
			close(OUT);
			
			#===ログ更新===#
			open(IN,"< php/$in{'bbs_no'}.cgi") || &error("Open error");
			eval{ flock (IN, 1); };
			foreach(<IN>){
				($no,$name,$pass,$message,$time)=split(/<>/);
				if($no==0){
					$message=$in{'message'};
					$name=$in{'name'};
					$flag="1";
				}
				push(@new_data,"$no<>$name<>$pass<>$message<>$time<>\n");
			}
			close(IN);
			if(!$flag){&error("そんな記事あらへんで～");}
			
			open(OUT,"> php/$in{'bbs_no'}.cgi") || &error("Write error");
			eval{ flock (OUT, 2); };
			print OUT @new_data;
			close(OUT);
			
			#===表示===#
			print <<"EOM";
			<center>
			<table border=0 cellspacing="5" cellpadding="0" width=300><tr>
			<td><center><h3><font color=#ff3300>スレッドの内容を変更しました。</font></h3></center></td>
			</tr></table>
			</center>
EOM
		}else{
			#===全体ログ===#
			open(IN,"< php/all_log.cgi") or &error("Open error");
			eval{ flock (IN, 1); };
			foreach(<IN>){
				($no,$title,$name,$pass,$senyou,$last,$laster,$res)=split(/<>/);
				if($in{'bbs_no'}==$no){
					$flag="1";
					last;
				}
			}
			if(!$flag){&error("隊長！そんなスレ見つかりません！");}
			close(IN);

			#===ログ===#
			open(IN,"< php/$in{'bbs_no'}.cgi") || &error("Open error");
			@data=<IN>;
			($no,$name,$pass,$message,$time)=split(/<>/,$data[0]);
			close(IN);
			if(!$flag){&error("そんな記事あらへんで～");}
			
			#===表示===#
			$message =~ s/&lt;br&gt;/\n/g;
			if($senyou){$check=" checked";}
			print <<"EOM";
			<center>
			<table><tr>
			<form action="./bbs.cgi" method="POST">
			<input type="hidden" name="my_data" value="$in{'name'}<>$in{'pass'}<>$k_id<>$in{'town_no'}<>hensyuu<>">
			<input type="hidden" name="bbs_no" value="$in{'bbs_no'}">
			<input type="hidden" name="bbs_pass" value="$in{'pass'}">
			<input type="hidden" name="command" value="thread"><td>
			タイトル：<input type="text" name="title" size="60" value="$title"><br>
			<textarea cols="60" rows="10" name="message">$message</textarea><br>
			<input type="checkbox" name="senyou" value="on" id="senyou" $check><label for="senyou">メンバー専用</label>
			<input type="submit" value="新規投稿">
			</td></form></tr></table>
			</center>
EOM
		}
	}elsif($in{'command'} eq "res"){
		if($in{'bbs_pass'}){
			#===ログ更新===#
			open(IN,"< php/$in{'bbs_no'}.cgi") || &error("Open error");
			foreach(<IN>){
				($no,$name,$pass,$message,$time)=split(/<>/);
				if($no==$in{'no'}){
					if($pass){
						if($in{'pass'} ne $pass and $in{'pass'} ne $admin_pass){&error("パスワードがちが～う！");}
					}else{
						if($in{'pass'} ne $admin_pass){&error("このレスにはパスワードが設定されていません。");}
					}
					$message=$in{'message'};
					$name=$in{'name'};
					$flag="1";
				}
				push(@new_data,"$no<>$name<>$pass<>$message<>$time<>\n");
			}
			close(IN);
			if(!$flag){&error("そんな記事あらへんで～");}
			
			open(OUT,"> php/$in{'bbs_no'}.cgi") or &error("Write error");
			eval{ flock (OUT, 2); };
			print OUT @new_data;
			close(OUT);
			
			print <<"EOM";
			<center>
			<table border=0 cellspacing="5" cellpadding="0" width=300><tr>
			<td><center><h3><font color=#ff3300>記事の内容を変更しました。</font></h3></center></td>
			</tr></table>
			</center>
EOM
		
		}else{
			#===ログ===#
			open(IN,"< php/$in{'bbs_no'}.cgi") || &error("Open error");
			@data=<IN>;
			close(IN);

			foreach(@data){
				($no,$name,$pass,$message,$time)=split(/<>/);
				if($no==$in{'no'}){
					$message =~ s/&lt;br&gt;/\n/g;
					$flag="1";
					last;
				}
			}
			if(!$flag){&error("そんな記事あらへんで～");}
			
			print <<"EOM";
			<center>
			<table><tr>
			<form action="./bbs.cgi" method="POST">
			<input type="hidden" name="my_data" value="$in{'name'}<>$in{'pass'}<>$k_id<>$in{'town_no'}<>hensyuu<>">
			<input type="hidden" name="bbs_pass" value="$in{'pass'}">
			<input type="hidden" name="command" value="res">
			<input type="hidden" name="no" value="$in{'no'}">
			<input type="hidden" name="bbs_no" value="$in{'bbs_no'}"><td>
			<textarea cols="60" rows="10" name="message">$message</textarea><br>
			<input type="submit" value="投稿する">
			</td></form></tr></table>
			</center>
EOM
		}
	}else{&error("なんじゃこりゃー！");}
	
	&hooter("top","トップへ","bbs.cgi");
    
	exit;
}

################
#-----消去-----#
################
sub delete{
	if($in{'command'} eq "thread"){
		#===全体ログ更新===#
		open(IN,"< php/all_log.cgi") or &error("Open error");
		eval{ flock (IN, 1); };
		@data=<IN>;
		close(IN);
		
		foreach(@data){
			($no,$title,$name,$pass,$senyou,$last,$laster,$res)=split(/<>/);
			if($in{'bbs_no'}==$no){
				if($pass){
					if($in{'pass'} ne $pass and $in{'pass'} ne $admin_pass){&error("パスワードがちが～う！");}
				}else{
					if($in{'pass'} ne $admin_pass){&error("このスレにはパスワードが設定されていません。");}
				}
				$flag="1";
				next;
			}
			push(@new_data,$_);
		}
		if(!$flag){&error("隊長！そんなスレ見つかりません！");}
		
		open(OUT,"> php/all_log.cgi") or &error("Write error");
		eval{ flock (OUT, 2); };
		print OUT @new_data;
		close(OUT);
		
		#===ログ削除===#
		unlink("php/$in{'bbs_no'}.cgi") or &error("Delete error");
		
		print <<"EOM";
		<center>
		<table border=0 cellspacing="5" cellpadding="0" width=300>
		<tr><td>
		<center><h3><font color=#ff3300>スレッドを削除しました。</font></h3></center>
		</td></tr>
		</table>
		</center>
EOM
	
	}elsif($in{'command'} eq "res"){
		#===ログ更新===#
		open(IN,"< php/$in{'bbs_no'}.cgi") or &error("Open error");
		eval{ flock (OUT, 1); };
		@data=<IN>;
		close(IN);
		
		foreach(@data){
			($no,$name,$pass,$message,$time)=split(/<>/);
			if($in{'no'}==$no){
				if($pass){
					if($in{'pass'} ne $pass and $in{'pass'} ne $admin_pass){&error("パスワードがちが～う！");}
				}else{
					if($in{'pass'} ne $admin_pass){&error("このレスにはパスワードが設定されていません。");}
				}
				$flag="1";
				next;
			}	
			push(@new_data,$_);
		}
		if(!$flag){&error("隊長！そんな記事見つかりません！");}

		open(OUT,"> php/$in{'bbs_no'}.cgi") or &error("Write error");
		eval{ flock (OUT, 2); };
		print OUT @new_data;
		close(OUT);
		
		#===全体ログ更新===#
		open(IN,"< php/all_log.cgi") or &error("Open error");
		eval{ flock (IN, 1); };
		@all_data=<IN>;
		close(IN);
		
		foreach(@all_data){
			($no,$title,$name,$pass,$senyou,$last,$laster,$res)=split(/<>/);
			if($in{'bbs_no'}==$no){
				chomp $res;
				$res--;
				$flag="1";
			}
			push(@new_all_data,"$no<>$title<>$name<>$pass<>$senyou<>$last<>$laster<>$res<>\n");
		}
		if(!$flag){&error("隊長！そんなスレ見つかりません！");}
		
		open(OUT,"> php/all_log.cgi") or &error("Write error");
		eval{ flock (OUT, 2); };
		print OUT @new_all_data;
		close(OUT);

		print <<"EOM";
		<center>
		<table border=0 cellspacing="5" cellpadding="0" width=300>
		<tr><td>
		<center><h3><font color=#ff3300>記事を削除しました。</font></h3></center>
		</td></tr>
		</table>
		</center>
EOM
	}else{&error("なんじゃこりゃあ～！");}
	
	&hooter("top","トップへ","bbs.cgi");
	
	exit;
}

################
#-----表示-----#
################
sub top{
	if($in{'bbs_no'} ne ""){
		open(IN,"php/all_log.cgi") || &error("Open error");
		foreach(<IN>){
			($bbs_no,$bbs_title,$bbs_name,$bbs_pass,$bbs_senyou,$bbs_last,$bbs_laster,$bbs_res)=split(/<>/);
			if($bbs_no eq $in{'bbs_no'}){
				if($bbs_senyou){
					open(IN,"< log_dir/php_member.cgi") or &error("Open error");
					eval{ flock (IN, 1); };
					@php_mamber=<IN>;
					close(IN);
					
					$flag = '';
					foreach(@php_mamber){
						chomp $_;
						if($in{'name'} eq $_){$flag = 1;}
					}
					if(!$flag){&error("メンバー以外は見れません。");}
				}
				last;
			}
		}
		close(IN);
		
		#===ログ表示===#
		open(IN,"php/$in{'bbs_no'}.cgi") || &error("Open error");
		foreach(<IN>){
			($no,$name,$pass,$message,$time)=split(/<>/);
			$message =~ s/&lt;br&gt;/<br>/g;
			if($name ne $admin_name){
				$message = &tag($message);
			}
			
			@week_day=("日","月","火","水","木","金","土");
			($sec,$min,$hour,$day,$mon,$year,$week)=localtime($time);
			$year-=100;
			$year=sprintf("%02d",$year);
			$sec=sprintf("%02d",$sec);
			$min=sprintf("%02d",$min);
			$hour=sprintf("%02d",$hour);
			$day=sprintf("%02d",$day);
			$mon=sprintf("%02d",$mon+1);
			$time="$year/$mon/$day/($week_day[$week])$hour:$min:$sec";
			
			if($no==0){
				$title = <<"EOM";
<table width="100%" cellpadding="5" cellspacing="0" style="font-size:14px;border: solid 3px #8080C0;">
<tr bgcolor="#8080C0">
<td align="left"><font color="#ffffff"><b>$name</b>さん</font></td>
<td align="right"><font color="#ffffff">$time</font></td>
</tr>
<tr>
<td bgcolor="#ffffff" colspan="2">$message</td>
</tr>
</table><br>
EOM
			}else{
				$naiyo .= <<"EOM";
<table width="100%" cellpadding="5" cellspacing="0" style="font-size:13px;border: solid 3px #DCDCED;">
<tr bgcolor="#DCDCED">
<td align="left"><font color="#ffffff"><a name="#$no">ＮＯ.$no　　<b>$name</b>さん</font></a></td>
<td align="right"><font color="#ffffff">$time</font></td>
</tr>
<tr bgcolor="#ffffff">
<td colspan="2">
	<table width="100%" border="0" cellpadding="0" cellspacing="0">
	<tr>
	<td>$message</td>
	<td width="50px"><a href="./bbs.cgi?bbs_no=$in{'bbs_no'}&no=$no&mode=hensyuu&command=res&name=$in{'name'}&pass=$in{'pass'}&k_id=$in{'k_id'}&town_no=$in{'town_no'}"><img src="img/reload.gif" alt="編集します" border="0"></a>　<a href="./bbs.cgi?bbs_no=$in{'bbs_no'}&no=$no&mode=delete&command=res&name=$in{'name'}&pass=$in{'pass'}&k_id=$in{'k_id'}&town_no=$in{'town_no'}"><img src="img/delete.gif" alt="消去します" border="0"></a></td>
	</tr>
	</table>
</td>
</tr>
</table>
EOM
			}
		}
		close(IN);
		
		#===表示===#
		print <<"EOM";
		<center>
		<h1>$bbs_title</h1>
		$title
		$naiyo<br>
		<table><tr>
		<form action="./bbs.cgi" method="POST">
		<input type="hidden" name="my_data" value="$in{'name'}<>$in{'pass'}<>$k_id<>$in{'town_no'}<>submit<>">
		<input type="hidden" name="command" value="Re">
		<input type="hidden" name="bbs_no" value="$in{'bbs_no'}"><td>
		<textarea cols="60" rows="10" name="message"></textarea>
		<input type="submit" value="投稿する">
		</td></form></tr></table>
		</center>
EOM

		&hooter("top","トップへ","bbs.cgi");
	}else{
		#===全体ログ表示===#
		open(IN,"php/all_log.cgi") || &error("Open error");
		foreach(<IN>){
			($bbs_no,$bbs_title,$bbs_name,$bbs_pass,$bbs_senyou,$bbs_last,$bbs_laster,$bbs_res)=split(/<>/);
			if($bbs_senyou){$bbs_title.="（専）";}
			
			$bbs_title = &tag($bbs_title);
			
			@week_day=("日","月","火","水","木","金","土");
			($sec,$min,$hour,$day,$mon,$year,$week)=localtime($bbs_last);
			$year-=100;
			$year=sprintf("%02d",$year);
			$sec=sprintf("%02d",$sec);
			$min=sprintf("%02d",$min);
			$hour=sprintf("%02d",$hour);
			$day=sprintf("%02d",$day);
			$mon=sprintf("%02d",$mon+1);
			$bbs_last="$year/$mon/$day/($week_day[$week])$hour:$min:$sec";
			
			$naiyo .= <<"EOM";
			<tr bgcolor="#ffffff">
			<td><font size="3">$bbs_no</font></td>
			<td align="right">
				<table width="100%" border="0" cellpadding="0" cellspacing="0">
				<tr>
				<td><a href="./bbs.cgi?bbs_no=$bbs_no&name=$in{'name'}&pass=$in{'pass'}&k_id=$in{'k_id'}&town_no=$in{'town_no'}"><font size="4">$bbs_title</font></a></td><td width="50px"><a href="./bbs.cgi?bbs_no=$bbs_no&mode=hensyuu&command=thread&name=$in{'name'}&pass=$in{'pass'}&k_id=$in{'k_id'}&town_no=$in{'town_no'}"><img src="img/reload.gif" alt="編集します" border="0"></a>　<a href="./bbs.cgi?bbs_no=$bbs_no&mode=delete&command=thread&name=$in{'name'}&pass=$in{'pass'}&k_id=$in{'k_id'}&town_no=$in{'town_no'}"><img src="img/delete.gif" alt="消去します" border="0"></a></td>
				</tr>
				</table>
			</td>
			<td><font size="3">$bbs_name</font></td>
			<td><font size="2">$bbs_last<br>$bbs_laster</font></td>
			<td><font size="3">$bbs_res</font></td>
			</tr>
EOM
		}
		close(IN);
		
		print <<"EOM";
		<center>
		<h1>近畿地方　ＰＨＰver　開発掲示板</h1>
		<h3>メンバー登録したい方は「チャゲ」へメールください。</h3>
		<table width="90%" border="1" cellpadding="5" cellspacing="0">
		<tr bgcolor="#eeeeee">
		<td width="25px">No</td>
		<td>Title</td>
		<td width="100px">Starter</td>
		<td width="150">Last</td>
		<td width="50px">Replies</td>
		</tr>
		$naiyo
		</table>
		<hr>
		<table>
		<tr>
		<form action="./bbs.cgi" method="POST">
		<input type="hidden" name="my_data" value="$in{'name'}<>$in{'pass'}<>$k_id<>$in{'town_no'}<>submit<>">
		<input type="hidden" name="command" value="new">
		<td>
		タイトル：<input type="text" name="title" size="60"><br>
		<textarea cols="60" rows="10" name="message"></textarea><br>
		<input type="checkbox" name="senyou" value="on" id="senyou"><label for="senyou">メンバー専用</label>
		<input type="submit" value="新規投稿">
		</td>
		</form>
		</tr></table>
		</center>
EOM
		
		&hooter("login_view","町に戻る");
	}
	
	exit;
}
