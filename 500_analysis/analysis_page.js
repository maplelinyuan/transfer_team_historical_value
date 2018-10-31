home_odd = 2.50;
away_odd = 2.70;
home_need_num = 4;

home_score = 0;
away_score = 0;
trs = $('#team_jiaozhan table tr');
inc = 0;
home_count = 0;
trs.each(function(){
	if ($(this).attr('class') === '' || !$(this).is(':visible')) return true;
	if (home_count === home_need_num) return false;
	tds = $(this).find('td');
	class_len = tds.eq(2).find('a').children('span').attr('class').split(' ')[1].length;
	score = tds.eq(2).find('a').children('em').text();
	home_goal = parseInt(score.split(':')[0]);
	away_goal = parseInt(score.split(':')[1]);
	if (class_len === 0){
		is_home = false;
		home_net_goal = away_goal - home_goal;
        if (Math.abs(home_net_goal) > 3){
			add_score = Math.abs(home_net_goal) - 3;
        } else {
			add_score = 0;
        }
		if (inc === 0){
			if (home_net_goal > 0){
				home_score += 3;
				home_score += add_score;
			} else if (home_net_goal < 0) {
                away_score += 3;
				away_score += add_score;
            }
        } else {
			return true;
        }
    } else{
		is_home = true;
		home_net_goal = home_goal - away_goal;
		if (Math.abs(home_net_goal) > 3){
			add_score = Math.abs(home_net_goal) - 3
        } else {
			add_score = 0;
        }
		if (home_net_goal > 0){
			home_score += 3;
            home_score += add_score;
        } else if (home_net_goal < 0) {
			away_score += 3;
            away_score += add_score;
        }
		home_count++;
    }
// 	console.log(is_home)
	inc++;
})

trs_1 = $('#team_zhanji_1 table tr');
inc = 0;
home_count = 0;
trs_1.each(function(){
	if ($(this).attr('class') === '' || !$(this).is(':visible')) return true;
	if (home_count === home_need_num) return false;
	tds = $(this).find('td');
	class_len = tds.eq(2).find('a').children('span').attr('class').split(' ')[1].length;
	score = tds.eq(2).find('a').children('em').text();
	home_goal = parseInt(score.split(':')[0]);
	away_goal = parseInt(score.split(':')[1]);
	if (class_len === 0){
		is_home = false;
		home_net_goal = away_goal - home_goal;
        if (Math.abs(home_net_goal) > 3){
			add_score = Math.abs(home_net_goal) - 3;
        } else {
			add_score = 0;
        }
		if (inc === 0){
			if (home_net_goal > 0){
				home_score += 3;
				home_score += add_score;
			} else if (home_net_goal === 0) {
                home_score += 1;
            }
        } else {
			return true;
        }
    } else{
		is_home = true;
		home_net_goal = home_goal - away_goal;
		if (Math.abs(home_net_goal) > 3){
			add_score = Math.abs(home_net_goal) - 3;
        } else {
			add_score = 0;
        }
		if (home_net_goal > 0){
			home_score += 3;
            home_score += add_score;
        } else if (home_net_goal === 0) {
			home_score += 1;
        }
		home_count++;
    }
// 	console.log(is_home)
	inc++;
})
trs_2 = $('#team_zhanji_0 table tr');
inc = 0;
home_count = 0;
trs_2.each(function(){
	if ($(this).attr('class') === '' || !$(this).is(':visible')) return true;
	if (home_count === home_need_num) return false;
	tds = $(this).find('td');
	class_len = tds.eq(2).find('a').children('span').attr('class').split(' ')[1].length;
	score = tds.eq(2).find('a').children('em').text();
	home_goal = parseInt(score.split(':')[0]);
	away_goal = parseInt(score.split(':')[1]);
	if (class_len !== 0){
		is_home = false;
		home_net_goal = home_goal - away_goal;
        if (Math.abs(home_net_goal) > 3){
			add_score = Math.abs(home_net_goal) - 3;
        } else {
			add_score = 0;
        }
		if (inc === 0){
			if (home_net_goal > 0){
				away_score += 3;
				away_score += add_score;
			} else if (home_net_goal === 0) {
                away_score += 1;
            }
        } else {
			return true;
        }
    } else{
		is_home = true;
		home_net_goal = away_goal - home_goal;
		if (Math.abs(home_net_goal) > 3){
			add_score = Math.abs(home_net_goal) - 3;
        } else {
			add_score = 0;
        }
		if (home_net_goal > 0){
			away_score += 3;
            away_score += add_score;
        } else if (home_net_goal === 0) {
			away_score += 1;
        }
		home_count++;
    }
// 	console.log(is_home)
	inc++;
});
score_differ = home_score - away_score;
console.log(home_score);
console.log(away_score);
console.log('主客差：' + score_differ);
if (score_differ > 0) {
    max_home_odd = home_odd - score_differ * 0.10;
    console.log('主最大赔率：' + (max_home_odd).toFixed(2));
    if (max_home_odd < 1){
        console.log('不确定~~')
    }
} else if (score_differ < 0) {
    max_away_odd = away_odd - score_differ * -0.10;
    console.log('客最大赔率：' + (max_away_odd).toFixed(2));
    if (max_away_odd < 1){
        console.log('不确定~~')
    }
} else{
    console.log('主 客最大赔率：2.50 ：2.70');
}

