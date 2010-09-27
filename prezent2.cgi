#!/usr/bin/perl

require './town_ini.cgi';
require './town_lib.pl';
&decode;

#メンテチェック
if($mente_flag == 1 && $in{'admin_pass'} eq "" && $in{'mode'} ne ""){&error("$mente_message")}
#制限時間チェック
$seigenyou_now_time = time;
$ato_nanbyou=$koudou_seigen-($seigenyou_now_time - $access_byou);
if($seigenyou_now_time - $access_byou < $koudou_seigen){&error("まだ行動できません。あと$ato_nanbyou秒お待ちください。")}

if($in{'mode'} eq "get"){&get;}
else{&top;}
exit;

sub top{
	&header(item_style);
	
	print <<"EOM";
TOWN内のどこかに隠されたパスワードを入力してください。<br>
先着５名様だとさらにいいことが！<br>
<form action="prezent2.cgi" method="POST">
<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>get<>">
<input type="text" name="pp" size="20"><br>
欲しいもの：<select name="sentaku"><option value="money">お金</option><option value="kpoint">Kポイント</option></select><br>
<input type="submit" value="プレゼントゲット">
</form>
EOM
	
	&hooter("login_view","町に戻る");
}

sub get{
	if($in{'pp'} ne "$k_id$syoukai_id"){
		&error("パスが違います。");
	}
	
    open(IN,"log_dir/prezent2.cgi") || &error("open Error : log_dir/prezent2.cgi");
	eval "flock(IN, 2);";
	@member=<IN>;
	close(IN);
	
	foreach(@member){
		chomp $_;
		if($name eq $_){&error("一人一回");}
		push @new_member,"$_\n";
	}
	unshift @new_member,"$name\n";
	$ninzuu = @new_member;
    
	open(OUT,">log_dir/prezent2.cgi") || &error("Write Error : log_dir/prezent2.cgi");
	eval{ flock (OUT, 2); };
	print OUT @new_member;
	close(OUT);
	
	if($in{'sentaku'} eq "money"){
		if($ninzuu <= 5){
			$money += 10000000;
			$message = "先着５名ですので、１０００万円ゲットしました。";
		}else{
			$money += 1000000;
			$message = "１００万円ゲットしました。";
		}
	}else{
		if($ninzuu <= 5){
			$kpoint += 1000;
			$message = "先着５名ですので、Kポイントが１０００あがりました。";
		}else{
			$kpoint += 100;
			$message = "Kポイントが１００あがりました。";
		}
    }
        
	&temp_routin;
	&log_kousin($my_log_file,$k_temp);
	
	&hooter("login_view","街へ戻る");
}
