import pandas as pd
import folium
from folium.plugins import MarkerCluster

def cars_by_country_map(df_path, JSON_file_path):
  df = pd.read_csv("path")

  country_counts = df['country_of_origin'].value_counts().to_dict()
  total_cars = sum(country_counts.values())
  
  # Pre-built dataset mapping countries to coordinates and flag image URLs
  country_data = {
      'South Korea': {'coordinates': (37.5665, 126.9780), 'flag_url': 'data:image/png;base64,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'},
      'Japan': {'coordinates': (36.2048, 138.2529), 'flag_url': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAARMAAAC3CAMAAAAGjUrGAAAAflBMVEX///+8AC23AAC7ACe7ACm4ABW5ABu4ABC6ACO5ABm7ACi4ABO6ACL46u3sx83NYXG3AAfnvcL14OTiqLH78fPKVGbEOE/9+PnGQFbjrbX35OjnuL/x09jsxszpv8XfoarSc4HXhZHAHj3CK0bbkJvQanm/DzbUeYbemqS/FjiKuKh1AAADpUlEQVR4nO3diXaiMBSA4QJCUFxwQ63WurTavv8LDtSZozZxipiQE/p/D+Dh3hOTS8jy9AQAAAAAAAAAAAAAAAAAAAqT3uplPRwO1y+r3sT2w1g3679usiBMRRIWEpGGQbZ57f/WzMz6272fRN1Oy7vU6nSjxN9v+zPbD1i74aAtutfZuMpMV7QHS9sPWafVMUnim/n4Jw6Tzcr2o9ZkPfe7PybkpOtna9uPW4PlTgQlM1IIxK7pf6H+TtzuRNRaYte3/dgG9ab+vRn5yoo/7dl+dFM+xM8dq1qcfth+eCN6WVIxI4Uka2BTWST3dK2yQCxsh6DbMX0oI4V0YzsIrWbz9sMp8bx21qB6v/dZtkj7v/izMZ3KKHqsKzkLopHtYPQYJVWKErWWaERSRqG+lORJCRuQlF6kMyV5UiLn+5SZ19GaEi//PddHn6xqOX9bnNkO6jHvkfaUeF70bjusRywer15V0rHtwKp79o2kxPP8Z9uhVbbXVat9F+xth1bVW2goJZ4XvtkOrhpj/5yC72bpNjf1zykEc9vhVbEUBlPiecLF6XxPb03/XetgO8D7jc11sCehe0VKbLaZ5A0lth3ivRamm0neUFybtN6ZbiZ5Q9nZDvI+fTMvOtdSt76ZDvRPEcjige0w7zGpo5nkDcWlNV5jHZ9zftZ2aTg2WtafuVTgT0y+/V3y3fnzLM0XJyehOy8973WMOoXYnZlZw69/Zy3PdqhlPdczEhdSVyZma+tOHOpQtnpWVpTR3doOtqRpPdVJIZ7aDrakQ11drEOzbXVVbAXfdrDl1DjsODPwrMxO2F8TbuzcWNc3FOeDsRv7Nhb1TBSctN2YlK1p8uRvTtyYQhmbWIdzS0ROyEmDckJ/ImHckVGfyKhjZbzvKPBeLGP+RMY8m4z5WBnz9jK+7yjwHVDG92IZ6wpkrD9RYJ2SjPVsMtY9KrA+VsY6agXW28vYl6HA/h0Z+7wUDM+2OTPDdsnwvtHUnVedC+wvlpndh+7MZNI1zitQ4FwLGeefKJg6J8e5CvbSxsh5ShvbYT2Gc7dks4PufrZzcP18Ns7xU+G8RwWt54ImjUgJ58cqcc6wAudRq+g4t/xoOwjdlnddHSILnDx87Afcg6DywH0Zopn3ZTxxr4oa9++ocE+TCvd5qayOYbl7345u7LrQ5Ot+wNtH33d+3f2AJ8U9kuLmPZIvzarjy7t13+hvzccZ99ICAAAAAAAAAAAAAAAAACD7A+PaSTdtOrdEAAAAAElFTkSuQmCC'},
      'Italy': {'coordinates': (41.8719, 12.5674), 'flag_url': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAARMAAAC3CAMAAAAGjUrGAAAAFVBMVEX///8AkkbOKzcAjz56uI/ehIjNHy1xf0V9AAAA/klEQVR4nO3QSQ0AIAADsHH6l4yKPUhaCc2oWTs9586aOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHy4ckD5KrN4eD2boIAAAAASUVORK5CYII='},
      'United States of America': {'coordinates': (37.0902, -95.7129), 'flag_url': 'data:image/png;base64,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'},
      'France': {'coordinates': (46.2276, 2.2137), 'flag_url': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAARMAAAC3CAMAAAAGjUrGAAAAFVBMVEX///8AJlTOESYAGU16gpXefILNABnwlnA6AAAA/klEQVR4nO3QSQ0AIAADsHH6l4yKPUhaCc2oWTs9586aOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHixIkTJ06cOHHy4ckD5KrN4eD2boIAAAAASUVORK5CYII=" class="YQ4gaf'},
      'China': {'coordinates': (35.8617, 104.1954), 'flag_url': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAARMAAAC3CAMAAAAGjUrGAAAAjVBMVEXuHCX//wDtACb72Q7uFSXuDSbuACX//ADvMCP+8gX83gv84Qr/+wD5wxH96wf+9QPzdR3wRCH96gjvOCL4rxTyZx7xVyD1jhn3rRX7zw/71w370w3wSyHyYh/2oRf5uhPxUiD0gxv1lBn0fBz6yRD5vhL2nRfzbh3vMiP3pxTwPyHyXh/1kBr1iRn4tBT+HvuxAAAEtklEQVR4nO3c61biMBQF4OaQlGKBcldRLgqIgvr+jzdJb4B2IOkCacL+/syapbLa3ZwkTUo9DwAAAABunLj2AVQPLUb82sdQFWnzEF0WIJNEcC9IZsGDJkMkKfpmD30Sos0i/9rHUhl+xNjjaMxYj659KJUh1ixRQyY5ekoyCWUJXftYLky7x+RB2lDYeE1OtxX+rBsKTViuMX2/6FFdF80meqHIiUmu3XrVjtJCFA206oB7zTSQVicgIocj4XPW0MpETkxYfXknMxm5nIdCD4zplIFYLb+6RKqbfXc8Eo/k5f/QaShJudCUMdensfyZmU1M/QZzehj2kuvOWFe/GsS66XwmPZXJ1OA0SavSLMY38ehqdFfH//sfNySlY1Q8h7ru3flQmGTyVrIeqN3Plt9caTFp6chb3bKZjOuBCkXQUPMOofLoLbuB6Zc7I5qxKBCCtrW6Kz1vVjqMvZY7JXqVt8jeRM74XxzJhPfzG927cqcUr73V1Y2yI5HEVzlTbn+CsmWmtSvjD93tMilTPESdntVLtPQb30Uiz+q349de0KKXl55v5aizCms/jMO9TNj4549r4f2xUMRLc++vQyvXVOSwaejUULJZTJftXSdtZSjrukkiYXCqj+BC1pfqptuRKj4rl1XIq+lH8qF33UVH/m6fgu3n6sPKoYfv5q0nRFvNgURNcWaUNJnLHvzF0LyhE8kj177mVHZqUx1CLE9H8mnQX1JDbyuk0ujlRCLtrslJ0vhiR/qHqB8ei2RmtkHON5ZXToLT4P+RdEwrwYlIPDVVaRYncndyUuIu8p6KIplaORk9FxoWROL8zs1x1CrsTKycip6LX9ihtG65oeTP6x2qW3kfdya0Kh53nFlCLKG4dBhblSgeR4YqUTTqxMVjnon4ciOUgzW3t/27wolx8VB76ETB0a50GnPa39KYmU/tSxVc5YhtnsHSlxeZnvNl1cj0/MTCjdGKvrMI0mVosRuHtoaFoCZ/CweKh6Lk/HvveaugTprJt3ZD4ckmkPysJ/mPz4PgMkf7J/goOf3B/h0fBcmmoN7DsupTJoOH79XyUf1Ru1mvy3vqixzt30iWT+rDw7Pn9BGHov1lP7HXNccNzOYxmdQ69dj71SBo24xbj/bnBHt7IwurBx8+Z2rLvOCqxgvY2sWjmtZnmkhvY3UknqwROSkp/BGne70nzfPPekkysf35UIpa/n8HT+oa7U1kyzAGjauK+PPXsRMQNDWYbaiROFK9iuXz+1N7fAZnp0b1MH7c6aZXow7IrmkmO2vahMzudnJG1EvqUM5tjj6/c1NGWcmgdHI2T13PClXyCw0Qyg/0ZvkE7Yw2XvwQBg1Lf4nDQY3Wlki8qyWkax9KVYiJektB0GNsiUwy+QaIE+v0Z+Kny7h3c6ffVmBkt3vYngZIJbZ7J4wUbhGKl7zaINF8vO9e+2gqgbJ95dbIR4cSi5/Vb6hHa40fF3WVWLCnzw2pB1du+6m3PXwkVMGoPVTL117PKO1AZK+C14L+wL3yL3xwFn258a2Ds0JvAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIf+AetuKcIDJwwmAAAAAElFTkSuQmCC'},
      'Germany': {'coordinates': (51.1657, 10.4515), 'flag_url': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAASIAAACuCAMAAAClZfCTAAAAElBMVEUAAAD/zgDdAADnAADaAAD/2AAtsSEoAAAA+ElEQVR4nO3QMQGAMAAEsYeCf8tIuI0pkZANAAAAAAAAAAAAAAAAAAAAgB8dwm6CoqQoKUqKkqKkKClKipKipCgpSoqSoqQoKUqKkqKkKClKipKipCgpSoqSoqQoKUqKkqKkKClKipKipCgpSoqSoqQoKUqKkqKkKClKipKipCgpSoqSoqQoKUqKkqKkKClKewh7CbsIipKipCgpSoqSoqQoKUqKkqKkKClKipKipCgpSoqSoqQoKUqKkqKkKClKipKipCgpSoqSoqQoKUqKkqKkKClKipKipCgpSoqSoqQoKUqKkqKkKClKipKipCgpSoqSoqQoKUofMGTNC8HkSxoAAAAASUVORK5CYII='},
      'Czechia': {'coordinates': (49.8175, 15.4730), 'flag_url': 'data:image/png;base64,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'},
      'Spain': {'coordinates': (40.4637, -3.7492), 'flag_url': 'data:image/png;base64,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'},
      'Romania': {'coordinates': (45.9432, 24.9668), 'flag_url': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAARMAAAC3CAMAAAAGjUrGAAAAG1BMVEUAK3/OESb80RYAJIFpaWP/1wr+2BXcXCHNACZkkvHSAAABAElEQVR4nO3QRwEAIAwEsDKLf8WouF8iIVUxa5+ZcvuNmFyJEydOnDhx4sSJEydOnDhx4sSJEydOnDhx4sSJEydOnDhx4sSJEydOnDhx4sSJEydOnDhx4sSJEydOnDhx4sSJEydOnDhx4sSJEydOnDhx4sSJEydOnDhx4sSJEydOnDhx4sSJEydOnDhx4sSJEydOnDhx4sSJEydOnDhx4sSJEydOnDhx4sSJEydOnDhx4sSJEydOnDhx4sSJEydOnDhx4sSJEydOnDhx4sSJEydOnDhx4sSJEydOnDhx4sSJEydOnDhx4sSJEydOnDhx4sSJEydOnDhx4sSJEye5kw8x5tcsm2OWvgAAAABJRU5ErkJggg=='},
      'India': {'coordinates': (20.5937, 78.9629),'flag_url':  'data:image/png;base64,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'},
      'United Kingdom': {'coordinates': (55.3781, -3.4360), 'flag_url': 'data:image/png;base64,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'},
      'Sweden': {'coordinates': (60.1282, 18.6435), 'flag_url': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAARwAAACxCAMAAAAh3/JWAAAAHlBMVEUAaqf+zAD/0QAAaKlPfJZggpAAZqpdgZFKepiBj4EDfUmrAAABn0lEQVR4nO3ay43CUBBFwYc9/PJPeIig8IKWkDmVQKvP+q41Y79ul3e26z50/csVB4oDxYHiQHGgOFAcKA4UB4oDxYHiQHGgOFAcKA4UB4oDxYHiQHGgOFAcKA4UB4oDxYHiQHGgOFAcKA4UB4oDxYHiQHGgOFAcKA4UB4oDxYHiQHGgOFAcKA4UB4oDxYHiQHGgOFAcKA4UB4oDxYHiQHGgOFAcKA4UB4oDxYFzxNln3O4H4txvQ9c/ZP3NeDwPxHk+hq5/yNqmvG3zqvPl1oEfflZxoDhQHCgOFAeKA8WB4kBxoDhQHCgOFAeKA8WB4kBxoDhQHCgOFAeKA8WB4kBxoDhQHCgOFAeKA8WB4kDLLmgTCK1JYWzBe4od8pDiQHGgOFAcKA4UB4oDxYHiQHGgOFAcKA4UB4oDxYHiQHGgOFAcKA4UB4oDxYHiQHGgOFAcKA4UB4oDxYHiQHGgOFAcKA4UB4oDxYHiQHGgOFAcKA4UB4oDxYHiQHGgOFAcKA4UB4oDxYHiQHGgOFAcKA4UB4oDxYHiQHGgOHCKOP/ItlPLsoEE4gAAAABJRU5ErkJggg=='},
      'Russia': {'coordinates': (61.5240, 105.3188), 'flag_url': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAARMAAAC3CAMAAAAGjUrGAAAAD1BMVEX///8AOabVKx4AMqTTKxXmvQ9FAAAA9UlEQVR4nO3QsQGAMAzAsBT4/2b2eOwqnaAZAAAAAAAAAAAAAAAAAAAAAK69bHPYnJSTclJOykk5KSflpJyUk3JSTspJOSkn5aSclJNyUk7KSTkpJ+WknJSTclJOykk5KSflpJyUk3JSTspJOSkn5aSclJNyUk7KSTkpJ+WknJSTclJOykk5KSflpJyUk3JS87HNw+aknJSTclJOykk5KSflpJyUk3JSTspJOSkn5aSclJNyUk7KSTkpJ+WknJSTclJOykk5KSflpJyUk3JSTspJOSkn5aSclJNyUk7KSTkpJ+WknJSTclJOykk5KSflpJyUk/oBg6TI4mvpq6EAAAAASUVORK5CYII='},
      'Tunisia': {'coordinates': (33.8869, 9.5375), 'flag_url': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAARMAAAC3CAMAAAAGjUrGAAAAh1BMVEXnABP////mAADnAA3tZWvnAAnnAAX/+vv97e75z9HnAAz+9fb3u77pICv+7/D//f7tWWDsSFDsUln3wMPrP0fxhov3uLvsTlX73d/vdXrpKzXyjpLoGCXwf4TqMjv4xsn0oaXuaW/95OboDR31rrHzk5frOULzmZ361tntX2XpJTDrQknvcHaIZcxIAAAFAUlEQVR4nO2da3viOAyFQSFAgHBLSoFyh9JS+v9/3yZl2NqSwm23Q23O+2nagT7RwZYl2RalEgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAfilBWKVqGNz7MX4HDfoiTnv9Xhoffgjv/VB3JMjs/xgtolX5m1W0GM2y3z/kkMkEWY+SZlmjmUzXjydLSDSNVD2OvE8faxKFNNvUTiqSU9vMqHrvR/1LNGibnBXkQJJS496P+zeguHWhIjmtmO79wD8O0WvnCkkyXslzVSgdXqdIxmrvsygBvVytSM6Lv+tyleY3SVIuz31dgCiu3yhJuVz309VSr8C5tqPF06i/3+77o6dF1NZf1Ol5KAp1NVNr8zyK/0r8wvDwj/U0UeO5rneiqJJEn0q2l2eGSy3u900UepY2DmZFeV4my2wg3/DslSg0E9NhPj6Z4oU0FotUbeaRKEHAV5z67mzSG1JXvCvwJ04h7h4GarwekEmQ5QEb9r7Im4FCb8y0keJHMkFKz2+DYb3ertdXyWIZE1Xpk63fb56IQj3brmYqDQupMY2Yzxm+jYm2rBLnSe5DtluoT4RZAX1s1IAu6tKavdsLTWhhG1USVlFVWXiPg2XPJPVh9oSxPXHWPJsLaFSoSM6A7OkTu1+lZbnwmH/MdDZZbnctRzN3fqAwB1sRkowLkj4Te0l2Phu0Q5ONkKQoWWZDxfzB9SClujetEYsGG0U8jikgdbvARFaNnidxPA3q2ktUES2nB0owOWVLELKEpkKXVbDXLqc9dk06ZvtXxLe+KhSXL+HF5YFife7cwcq4pEJnYpU/DB3WJJyZloztYCsgUVPJVmq6aJNw5m7cZk0dHmuRdKiZJgFdEK+4PHms4GRn2xGUpKl5REd7/tuW3AJxN0QJAiNTaZ4fJoco1/bLyZKm8oXNhqsrj1WYHnBNlA2LQ+T/7+hqtnZElMrXZZGOq2Gb9YmzTIeWiqWH1zTW+fBqD7qZIJl/UTcPnXUoZJZFYnu0i9jE0I127U2fDiVb0ksrfNQ5gxmdrPjU0U73HccS0bGGXRSvOBuhmHazuD4ca5aKSkJ1XJA2c4/tCsHEcKML5k6UxUQs1ywONqlN3Fx4QnPFGDFN5Eo8fBXbfNp6/YfUzUiW+oYNfaYJKzi+v4zlcVj9KIL691yBdoYNW9tgejf+L3qakHLm0wr5OGKauQFVDBtY1vbtKKJpqeB4gdhRNRHu2A2ssGxsj4OjJknxNQxLUsHSUU0wTgT/2Z+UPPQnWHcEPxqfbN2MTxDHKpzIdxoPmu8gL1Ywax8dtrnzsPUTs87Ggiw1InuEOhvqsYL/oW7f8a1uj/0dhZv2AS+55OOsO8F+sQrOFUhw/kQSrE1TEn5OqXrbOaWO0+eUcJ5NoWpFXDj3+AXOx0p+4By1+9dVcN5e0uD3MrhJ5+5lbPy7l3HJ/R1x7++b99TD+zuX3vNS7577es9LZLrafcCGeh/wgyj18z7gFfdGX/m9Ue5q/Jg5ObhfLLnxHvpOvMvd8poE/QoUtL4Wre2pvhZKbcmvvhbX9j/5fIT+Jyf65ExYn5zJNFHzQv8kycMU9FMSoO+WAvqzKaCPn8ZN/R6V/Mgrru4L2vG+L2gGTdA/VoA+wxpZMoN+1AL0LddAf3sVfA+CDr4voxB8rwoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8Mv5BxUYUPq7JIFVAAAAAElFTkSuQmCC'},
      'Ukraine': {'coordinates': (48.3794, 31.1656), 'flag_url': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAARMAAAC3CAMAAAAGjUrGAAAAD1BMVEUAV7f/1wAAULuln3f/2wCAuqzxAAAAzUlEQVR4nO3QsQGAMAzAsBT4/2b2eO0onaAZAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACASx62ednmY5vD5qSclJNyUk7KSTkpJ+WknJSTclJOykk5KSflpJyUk3JSTspJOSkn5aSclJNyUk7KSTkpJ+WknJSTclJOykk5KSflpJyUk3JSTspJOSkn5aSclJNyUk7KSTkpJ+WknJSTclJOykk5KSflpJyUk3JSTspJOSkn5aSclJNyUk7KSTkpJ+WknJSTclJOykk5KSflpH7zk2pa0LCuDAAAAABJRU5ErkJggg=='}
  }
  
  # base map with OpenStreetMap tiles
  m = folium.Map(location=[0, 0], zoom_start=2)
  
  # bins for legend
  max_count = max(country_counts.values())
  legend_bins = [x for x in range(0, max_count + 500, 500)]
  
  # Choropleth layer to color countries based on count of cars
  choropleth = folium.Choropleth(
      geo_data= JSON_file_path,
      name='choropleth',
      data=country_counts,
      key_on='feature.properties.name',
      fill_color='YlGnBu',
      fill_opacity=0.7,
      line_opacity=0.2,
      legend_name='Count of Cars by Country',
      bins=legend_bins,
      legend_kwds={'loc': 'bottomleft', 'title': 'Count of Cars', 'orient': 'vertical'}
  ).add_to(m)
  
  # markers for each country with the count and percentage of cars as pop-up
  marker_cluster = MarkerCluster().add_to(m)
  for country, data in country_data.items():
      count = country_counts.get(country, 0)
      percentage = (count / total_cars) * 100
      flag_url = data['flag_url']
      popup_text = (
          f'<div style="font-family: Arial; font-size: 14px; color: black; width: 200px;">'
          f'<img src="{flag_url}" style="float: right; margin-left: 5px; width: 30px; height: 20px; border: 1px solid black;">'
          f'<b>{country}</b><br>'
          f'Market Percentage: {percentage:.2f}%'
          f'</div>'
      )
      folium.Marker(
          location=data['coordinates'],
          popup=popup_text,
          icon=None
      ).add_to(marker_cluster)
  
  # Layer Control to toggle between Choropleth and MarkerCluster
  folium.LayerControl().add_to(m)
  
  m.save('cars_by_country_map.html')


df_path = r"EDA Data/EDA.csv"
JSON_file_path = r"EDA Data/custom.geo.json"
cars_by_country_map(df_path, JSON_file_path)
