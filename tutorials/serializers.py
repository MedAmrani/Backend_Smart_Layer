from rest_framework import serializers 
from tutorials.models import Covid
 
 

class CovidSerializer(serializers.ModelSerializer):

    class Meta:
        model = Covid
        fields = ('id',
                  'Date',
                  'Total_Cases',
                  'New_Cases',
                  'Total_Deaths',
                  'New_Deaths',
                  'Total_Recovred',
                  'New_Recovred',
                  'Eliminated_Cases',
                  'Active_Cases',
                  'Tanger_Tetouan_AlHoceima',
                  'Oriental',
                  'Rabat_Sale_Kenitra',
                  'BeniMellal_Khenifra',
                  'Casablanca_Settat',
                  'Marrakech_Safi',
                  'Draa_Tafilalet',
                  'Sous_Massa',
                  'Fes_Meknes',
                  'Guelmim_OuedNoun',
                  'Laayoune_SaguiaalHamra',
                  'EdDakhla_OuededDahab'
                
                  )
    
