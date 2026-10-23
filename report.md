## 6.2 Interpret each result
- The probability of a large flow is 0.078618, so about 7.9% of records are large flows and the probability of a large average bytes per packet is 0.023592 or 2.4% which have a large average packet size. We can conclude that this network is highly dominated by small packets size and small flows, showing that higher volume dosen't usually mean large packets size.

## 6.4 Calculate P(Y = Allowed | F = Large) and compare it with the overall allowance probability in these M records.
- We got P(Allowed | F = Large) is 1.0 which is 100% and overall P(Y = Allowed) is 0.57 which is 57%. And in here, large flows are treated differently then regular traffic. Infact if we look at the table every large traffic flows are allwed. This mean that the two events P(Allowed) and P(Large flows) are dependent on each other.

## 6.5 Explain how a flow can have many bytes but a small average bytes per packet. Describe how changing the<br>
## category cutoffs could change your probability tables. Explain why this analysis describes randomly selected
## records rather than randomly selected individual packets. 
- We calculated that average bytes per packets = total bytes / packets. So, imagine a traffic flow that sends<br> 
1,000,000 bytes, but in 10,000 packets. Eventhough the total bytes is enormously large, the average bytes per packets is only 100 bytes/packets which is small.

- For this assginment, the cutoffs were given. And this cutoffs decided which bucket each record should land. So changing the category cutoff would change the probabiltiy table. If we look at our frequency table, F: Small and A: Small is 48209, which in thi case the cutoffs was 1000. if we change this to 500, then this would have fallen into a different category which is medium.

- The reason behind randomly selected records is to get equal weight. In our data, one row = one record = one flow, meaning that regardless of how many packets it contain, 1000 packets and 1 packet each still count as a single row or one random sample. If we randomly select individual packets instead, the big packet (100,000) would have more chance to be pick as random sample and dominate the whole sampling and the probability would come out differently.