require 'mechanize'

def getTitleKcal(url)
  agent = Mechanize.new
  page = agent.get(url)  

  page.search('tbody').search('tr')[1..-2].map{|tr|
    next if tr.search('td').length < 3
    next if tr.search('td a').first.nil?
    title = tr.search('td')[0].inner_text
    kcal = tr.search('td')[2].inner_text
    puts [title, kcal]
    [title, kcal]
  }.compact.to_h
end

root = 'http://www.mcdonalds.co.jp/quality/allergy_Nutrition/nutrient2.php?id=num'

(1..4).each {|i|
  puts i
  url = root.gsub('num', i.to_s)
  data = getTitleKcal(url)
  File.open("menu.txt", "a") do |f| 
    data.each{|menu, kcal|
      f.puts("{\"name\" : \"#{menu}\", \"kcal\" : \"#{kcal}\", \"yen\" : },")
    }
  end
  sleep 10
}

